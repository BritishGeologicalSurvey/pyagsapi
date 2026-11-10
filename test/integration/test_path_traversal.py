"""
Regression tests for the path traversal vulnerability in the file upload
handlers (validate and convert).

A malicious client can set the multipart ``filename`` to an absolute path
(e.g. ``/code/app/templates/landing_page.html``) or a relative path
containing ``..``.  The handlers must only ever use the basename so that the
uploaded bytes are written *inside* the per-request temporary directory and
can never escape it to overwrite application files or write elsewhere on disk.

See the fix in app/routes/validate.py and app/routes/convert.py
(``Path(file.filename).name``).
"""
import tempfile
from pathlib import Path

import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder

from test.fixtures import API_VERSION


@pytest.fixture
def pinned_tmp_dir(tmp_path, monkeypatch):
    """
    Pin the temporary directory created by the upload handlers to a known
    location so the test can inspect exactly where the upload was written.

    The handler creates its working directory with ``tempfile.mkdtemp()`` and
    schedules it for deletion once the response is sent.  By pinning it to
    ``tmp_path/handler`` we know:

    * a correctly-sanitised filename lands *inside* ``handler_dir`` and is
      removed with it when the request's background cleanup runs, whereas
    * a traversal/absolute filename that escaped would land *outside*
      ``handler_dir`` and survive cleanup, where the test can detect it.

    Every escape target used by the tests is kept within ``tmp_path`` so the
    tests stay hermetic even when run against the vulnerable code.
    """
    handler_dir = tmp_path / "handler"

    def fake_mkdtemp(*args, **kwargs):
        handler_dir.mkdir(exist_ok=True)
        return str(handler_dir)

    monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)
    return tmp_path, handler_dir


def _malicious_names(tmp_root, handler_dir):
    """
    Filenames that each try to escape ``handler_dir``, paired with the location
    the *vulnerable* code (``handler_dir / filename``) would write to.  All
    targets stay inside ``tmp_root`` so nothing pollutes the real filesystem.
    """
    return [
        # relative traversal one level up, out of handler_dir into tmp_root
        ("../escaped_relative.txt", tmp_root / "escaped_relative.txt"),
        # absolute path (pathlib discards handler_dir when the RHS is absolute)
        (str(tmp_root / "escaped_absolute.txt"), tmp_root / "escaped_absolute.txt"),
        # traversal buried in the middle of the name
        ("sub/../../escaped_mid.txt", tmp_root / "escaped_mid.txt"),
    ]


def _post(client, endpoint, filename, payload, with_checker):
    fields = [("files", (filename, payload, "text/plain"))]
    if with_checker:
        fields.append(("checkers", "ags"))
    mp_encoder = MultipartEncoder(fields=fields)
    return client.post(
        f"{API_VERSION}/{endpoint}/",
        headers={"Content-Type": mp_encoder.content_type},
        data=mp_encoder.to_string(),
    )


@pytest.mark.parametrize("endpoint, with_checker", [("validate", True), ("convert", False)])
def test_upload_filename_cannot_escape_tmp_dir(client, pinned_tmp_dir, endpoint, with_checker):
    """
    For each malicious filename the upload must not be written to the location
    the vulnerable code would have used (outside the handler's temp dir), and
    the handler's temp dir must be cleaned up afterwards.
    """
    tmp_root, handler_dir = pinned_tmp_dir

    for malicious_name, vuln_target in _malicious_names(tmp_root, handler_dir):
        # sanity: the target really is outside handler_dir
        assert handler_dir.resolve() not in vuln_target.resolve().parents

        response = _post(client, endpoint, malicious_name, b"<h1>PWNED</h1>{{ 7*7 }}",
                         with_checker)

        assert response.status_code == 200, f"{malicious_name!r} -> {response.status_code}"
        assert not vuln_target.exists(), (
            f"[{endpoint}] upload with filename {malicious_name!r} escaped to "
            f"{vuln_target} - filename path was not stripped"
        )

    # Nothing should remain under tmp_root except (possibly) the cleaned-up
    # handler dir.  Assert no stray files escaped anywhere beneath it.
    leaked = [p for p in tmp_root.rglob("*") if p.is_file()]
    assert leaked == [], f"[{endpoint}] files leaked outside temp dir: {leaked}"


@pytest.mark.parametrize("endpoint, with_checker", [("validate", True), ("convert", False)])
def test_upload_writes_basename_inside_tmp_dir(client, pinned_tmp_dir, monkeypatch,
                                               endpoint, with_checker):
    """
    White-box check: whatever path is supplied, the handler must write to
    ``<handler_dir>/<basename>`` and nowhere else.
    """
    tmp_root, handler_dir = pinned_tmp_dir
    written = []
    real_write_bytes = Path.write_bytes

    def spy_write_bytes(self, data):
        written.append(Path(self))
        return real_write_bytes(self, data)

    monkeypatch.setattr(Path, "write_bytes", spy_write_bytes)

    malicious_name = str(tmp_root / "sub" / ".." / ".." / "etc" / "escaped.ags")
    response = _post(client, endpoint, malicious_name, b"x", with_checker)

    assert response.status_code == 200
    assert written, f"[{endpoint}] handler did not write the uploaded file"
    for path in written:
        resolved = path.resolve()
        assert resolved.parent == handler_dir.resolve(), (
            f"[{endpoint}] file written to {resolved}, outside {handler_dir}"
        )
        assert resolved.name == "escaped.ags"
