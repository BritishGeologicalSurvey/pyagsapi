"""
Regression tests for temporary-directory cleanup in the validate and convert
endpoints.

Each request creates a working directory with ``tempfile.mkdtemp()``.  On the
success path it is removed by a background task once the response is sent; if
processing raises part-way through, the background task never runs, so the
handler must remove the directory itself (see the ``try/except`` in
app/routes/validate.py and app/routes/convert.py).  Without that, every failed
request would leak a temp directory.
"""
import tempfile

import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder

import app.routes.validate as validate_module
import app.conversion as conversion_module
from test.fixtures import API_VERSION


@pytest.fixture
def pinned_tmp_dirs(tmp_path, monkeypatch):
    """
    Make ``tempfile.mkdtemp()`` return known directories under ``tmp_path`` and
    record each one, so a test can assert whether they were cleaned up.
    """
    created = []

    def fake_mkdtemp(*args, **kwargs):
        d = tmp_path / f"handler{len(created)}"
        d.mkdir()
        created.append(d)
        return str(d)

    monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)
    return created


def _post(client, endpoint, fields):
    mp_encoder = MultipartEncoder(fields=fields)
    return client.post(
        f"{API_VERSION}/{endpoint}/",
        headers={"Content-Type": mp_encoder.content_type},
        data=mp_encoder.to_string(),
    )


def _raise(*args, **kwargs):
    raise RuntimeError("boom")


def test_validate_cleans_tmp_dir_on_error(client, pinned_tmp_dirs, monkeypatch):
    # Force a failure after the temp dir has been created.
    monkeypatch.setattr(validate_module, "validate_file", _raise)
    fields = [
        ("files", ("x.ags", b"DATA", "text/plain")),
        ("checkers", "ags"),
    ]

    with pytest.raises(RuntimeError):
        _post(client, "validate", fields)

    assert pinned_tmp_dirs, "handler never created a temp dir"
    for d in pinned_tmp_dirs:
        assert not d.exists(), f"temp dir {d} leaked after an error"


def test_convert_cleans_tmp_dir_on_error(client, pinned_tmp_dirs, monkeypatch):
    # Force a failure during conversion, after the temp dir has been created.
    monkeypatch.setattr(conversion_module, "convert", _raise)
    fields = [("files", ("x.ags", b"DATA", "text/plain"))]

    with pytest.raises(RuntimeError):
        _post(client, "convert", fields)

    assert pinned_tmp_dirs, "handler never created a temp dir"
    for d in pinned_tmp_dirs:
        assert not d.exists(), f"temp dir {d} leaked after an error"


@pytest.mark.parametrize("endpoint, extra", [("validate", [("checkers", "ags")]),
                                             ("convert", [])])
def test_tmp_dir_cleaned_on_success(client, pinned_tmp_dirs, endpoint, extra):
    # Control: a normal request must also leave no temp dir behind (the
    # background-task cleanup), confirming the error-path fix did not disturb it.
    fields = [("files", ("x.ags", b"DATA", "text/plain"))] + extra

    response = _post(client, endpoint, fields)

    assert response.status_code == 200
    assert pinned_tmp_dirs, "handler never created a temp dir"
    for d in pinned_tmp_dirs:
        assert not d.exists(), f"temp dir {d} was not cleaned up after success"
