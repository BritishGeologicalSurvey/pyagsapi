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


def get_request_url(request):
    """External calls need https to be returned, so check environment."""
    request_url = str(request.url)
    if AGS_API_ENV == "PRODUCTION" and request_url.startswith("http:"):
        request_url = request_url.replace("http:", "https:")

    return request_url
