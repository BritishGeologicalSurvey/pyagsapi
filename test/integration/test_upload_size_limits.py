"""
Regression tests for the upload size limits on the validate and convert
endpoints.

These guard against the denial-of-service vector where a client uploads a
very large file, many files, or a small ZIP that expands to a huge amount of
data (a "zip bomb").  The handlers must reject such requests with HTTP 413
*before* reading the payload into memory or extracting it to disk.

The size limits are monkeypatched to small values so the tests exercise the
checks without having to transfer large amounts of data.
"""
from io import BytesIO
from zipfile import ZipFile

import pytest
from requests_toolbelt.multipart.encoder import MultipartEncoder

import app.routes.utils as utils
from test.fixtures import API_VERSION


def _make_zip(entry_name, uncompressed_bytes):
    """Return the bytes of a ZIP containing one entry of the given size."""
    buf = BytesIO()
    with ZipFile(buf, "w") as zf:
        zf.writestr(entry_name, b"A" * uncompressed_bytes)
    return buf.getvalue()


def _post(client, endpoint, fields):
    mp_encoder = MultipartEncoder(fields=fields)
    return client.post(
        f"{API_VERSION}/{endpoint}/",
        headers={"Content-Type": mp_encoder.content_type},
        data=mp_encoder.to_string(),
    )


def _assert_413(response):
    assert response.status_code == 413, (
        f"expected 413, got {response.status_code}: {response.text[:200]}"
    )
    body = response.json()
    # Error response schema from app/routes/errors.py
    assert body["errors"][0]["error"] == "Payload too large"


@pytest.fixture
def tiny_limits(monkeypatch):
    """Shrink the size limits so small test payloads trip them."""
    monkeypatch.setattr(utils, "MAX_UPLOAD_SIZE", 100)
    monkeypatch.setattr(utils, "MAX_UNZIPPED_SIZE", 100)


@pytest.mark.parametrize("endpoint, extra", [("validate", [("checkers", "ags")]),
                                             ("convert", [])])
def test_single_file_too_large_rejected(client, tiny_limits, endpoint, extra):
    # A single file over MAX_UPLOAD_SIZE (100 bytes) must be rejected.
    payload = b"A" * 500
    fields = [("files", ("big.ags", payload, "text/plain"))] + extra
    response = _post(client, endpoint, fields)
    _assert_413(response)


@pytest.mark.parametrize("endpoint, extra", [("validate", [("checkers", "ags")]),
                                             ("convert", [])])
def test_combined_files_too_large_rejected(client, tiny_limits, endpoint, extra):
    # Each file is within the limit, but their combined size exceeds it.
    part = b"A" * 60  # 60 < 100, but 60 + 60 = 120 > 100
    fields = [
        ("files", ("a.ags", part, "text/plain")),
        ("files", ("b.ags", part, "text/plain")),
    ] + extra
    response = _post(client, endpoint, fields)
    _assert_413(response)


@pytest.mark.parametrize("endpoint, extra", [("validate", [("checkers", "ags")]),
                                             ("convert", [])])
def test_zip_bomb_rejected(client, monkeypatch, endpoint, extra):
    # The uploaded ZIP is small, but its uncompressed contents exceed
    # MAX_UNZIPPED_SIZE.  Leave MAX_UPLOAD_SIZE at its default so only the
    # zip-size check can fire.
    monkeypatch.setattr(utils, "MAX_UNZIPPED_SIZE", 100)
    zip_bytes = _make_zip("inner.ags", 5000)
    assert len(zip_bytes) < utils.MAX_UPLOAD_SIZE  # upload itself is tiny
    fields = [("files", ("bomb.zip", zip_bytes, "application/zip"))] + extra
    response = _post(client, endpoint, fields)
    _assert_413(response)


@pytest.mark.parametrize("endpoint, extra", [("validate", [("checkers", "ags")]),
                                             ("convert", [])])
def test_within_limits_not_rejected(client, tiny_limits, endpoint, extra):
    # A small file under the (shrunk) limit must still be processed normally.
    payload = b"A" * 10
    fields = [("files", ("small.ags", payload, "text/plain"))] + extra
    response = _post(client, endpoint, fields)
    assert response.status_code == 200, response.text[:200]
