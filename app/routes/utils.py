import os
import re

from fastapi import HTTPException, status

from app.model.schema import Checker
from app.checkers import check_ags, check_bgs
from app.version import API_VERSION
from .errors import error_responses

# Get AGS_API_ENV, defaults to DEVELOP if not set or not recognised.
AGS_API_ENV = os.getenv("AGS_API_ENV", "DEVELOP").upper()

AGS_API_VERSION = f"/v{API_VERSION.split('.')[0]}"

BOREHOLE_EXPORT_LIMIT = 50
# Base URLs only.  Query parameters are passed via requests' params= so that
# values (borehole IDs, polygon WKT) are URL-encoded and cannot be used to
# inject extra parameters into the upstream request.
BOREHOLE_VIEWER_URL = "https://gwbv.bgs.ac.uk/GWBV/viewborehole"
BOREHOLE_EXPORT_URL = "https://gwbv.bgs.ac.uk/ags_export"
BOREHOLE_INDEX_URL = "https://ogcapi.bgs.ac.uk/collections/agsboreholeindex/items"

# BGS LOCA IDs are numeric strings; reject anything else so user input cannot
# alter the upstream request.
_LOCA_ID_RE = re.compile(r"^\d+$")


def validate_loca_ids(bgs_loca_id):
    """Split a semicolon-separated list of borehole IDs and validate each is
    numeric.  Returns the list of IDs, or raises HTTP 422."""
    ids = bgs_loca_id.split(";")
    if not ids or not all(_LOCA_ID_RE.match(i) for i in ids):
        raise HTTPException(
            status_code=422,
            detail="Invalid borehole ID: expected one or more numeric IDs separated by ';'",
        )
    return ids


MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB mirroring the Javascript limit for the landing page
MAX_UNZIPPED_SIZE = 100 * 1024 * 1024  # 100 MB

log_responses = dict(error_responses)
log_responses["200"] = {
    "content": {"application/json": {}, "text/plain": {}},
    "description": "Return a log in json or text",
}

zip_responses = dict(error_responses)
zip_responses["200"] = {
    "content": {"application/x-zip-compressed": {}},
    "description": "Return a zip containing successfully converted files and log file",
}

pdf_responses = dict(error_responses)
pdf_responses["200"] = {
    "content": {"application/pdf": {}},
    "description": "Return a graphical log of AGS data in .PDF format",
}

ags_export_responses = dict(error_responses)
ags_export_responses["200"] = {
    "content": {"application/x-zip-compressed": {}, "application/json": {}},
    "description": (
        "Return a zip containing .ags file and metadata .txt file "
        "or a json response containing the borehole ID count"
    ),
}


checker_functions = {
    Checker.ags: check_ags,
    Checker.bgs: check_bgs,
}


def _payload_too_large(desc):
    """Build a 413 response matching the API's error schema."""
    return HTTPException(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        detail={
            "msg": "Payload too large",
            "error": "Payload too large",
            "desc": desc,
        },
    )


def check_file_size(upload_file, request):
    """Reject an individual uploaded file that is too large.

    The landing page rejects files over this size, the API mirrors that.
    ``UploadFile.size`` is populated by the multipart parser; guard against
    ``None`` so a missing size cannot raise a TypeError.
    """
    if upload_file.size is not None and upload_file.size > MAX_UPLOAD_SIZE:
        limit_mb = MAX_UPLOAD_SIZE // (1024 * 1024)
        raise _payload_too_large(f"Upload file must be {limit_mb} MB or smaller")


def check_total_size(files, request):
    """Reject a request whose uploaded files together are too large.

    Mirrors the landing page, which caps the combined size of all files, so
    that many individually-acceptable files cannot be used to exhaust memory.
    """
    total = sum((f.size or 0) for f in files)
    if total > MAX_UPLOAD_SIZE:
        limit_mb = MAX_UPLOAD_SIZE // (1024 * 1024)
        raise _payload_too_large(
            f"Total size of uploaded files must be {limit_mb} MB or smaller"
        )


def check_zip_size(zipfile, request):
    """Reject an uploaded ZIP whose total uncompressed size is too large.

    Guards against zip-bomb denial-of-service, where a small upload expands
    to a very large amount of data on disk / in memory.
    """
    total_uncompressed = sum(info.file_size for info in zipfile.infolist())
    if total_uncompressed > MAX_UNZIPPED_SIZE:
        limit_mb = MAX_UNZIPPED_SIZE // (1024 * 1024)
        raise _payload_too_large(
            f"Uncompressed ZIP contents must be {limit_mb} MB or smaller"
        )


def get_request_url(request):
    """External calls need https to be returned, so check environment."""
    request_url = str(request.url)
    if AGS_API_ENV == "PRODUCTION" and request_url.startswith("http:"):
        request_url = request_url.replace("http:", "https:")

    return request_url
