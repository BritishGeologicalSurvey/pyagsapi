import os

from app.model.schema import Checker
from app.checkers import check_ags, check_bgs
from app.version import API_VERSION
from .errors import error_responses

# Get AGS_API_ENV, defaults to DEVELOP if not set or not recognised.
AGS_API_ENV = os.getenv("AGS_API_ENV", "DEVELOP").upper()

AGS_API_VERSION = f"/v{API_VERSION.split('.')[0]}"

BOREHOLE_EXPORT_LIMIT = 50
BOREHOLE_VIEWER_URL = "https://gwbv.bgs.ac.uk/GWBV/viewborehole?loca_id={bgs_loca_id}"
BOREHOLE_EXPORT_URL = "https://gwbv.bgs.ac.uk/ags_export?loca_ids={bgs_loca_id}"
BOREHOLE_INDEX_URL = (
    "https://ogcapi.bgs.ac.uk/collections/agsboreholeindex/items?f=json"
    "&properties=bgs_loca_id&filter=INTERSECTS(shape,{polygon})&limit={borehole_export_limit}"
)

MAX_UPLOAD_SIZE = 150 * 1024 * 1024  # 50 MB mirroring the Javascript limit for the landing page
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


def check_file_size(upload_file, request):
    """Reject an uploaded file whose total uncompressed size is too large.

    The landing page rejects files over this size, the API mirrors that.
    """
    if upload_file.size > MAX_UPLOAD_SIZE:
        limit_mb = MAX_UPLOAD_SIZE // (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "msg": "Payload too large",
                "error": "Payload too large",
                "desc": (
                    f"Upload file must be {limit_mb} MB or smaller"
                ),
            },
        )


def check_zip_size(zipfile, request):
    """Reject an uploaded ZIP whose total uncompressed size is too large.

    Guards against zip-bomb denial-of-service, where a small upload expands
    to a very large amount of data on disk / in memory.
    """
    total_uncompressed = sum(info.file_size for info in zipfile.infolist())
    if total_uncompressed > MAX_UNZIPPED_SIZE:
        limit_mb = MAX_UNZIPPED_SIZE// (1024 * 1024)
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "msg": "Payload too large",
                "error": "Payload too large",
                "desc": (
                    f"Uncompressed ZIP contents must be {limit_mb} MB or smaller"
                ),
            },
        )


def get_request_url(request):
    """External calls need https to be returned, so check environment."""
    request_url = str(request.url)
    if AGS_API_ENV == "PRODUCTION" and request_url.startswith("http:"):
        request_url = request_url.replace("http:", "https:")

    return request_url
