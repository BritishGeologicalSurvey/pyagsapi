import requests

from fastapi import APIRouter, Response
from fastapi.exceptions import HTTPException

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.checkers import check_ags, check_bgs
from app.errors import error_responses
from app.model.schema import Checker, ResponseType
from app.model.queries import ags_log_query, response_type_query

BOREHOLE_EXPORT_LIMIT = 50
BOREHOLE_VIEWER_URL = "https://gwbv.bgs.ac.uk/GWBV/viewborehole?loca_id={bgs_loca_id}"
BOREHOLE_EXPORT_URL = "https://gwbv.bgs.ac.uk/ags_export?loca_ids={bgs_loca_id}"
BOREHOLE_INDEX_URL = ("https://ogcapi.bgs.ac.uk/collections/agsboreholeindex/items?f=json"
                      "&properties=bgs_loca_id&filter=INTERSECTS(shape,{polygon})&limit=10")

router = APIRouter()

log_responses = dict(error_responses)
log_responses['200'] = {
    "content": {"application/json": {}, "text/plain": {}},
    "description": "Return a log in json or text"}

zip_responses = dict(error_responses)
zip_responses['200'] = {
    "content": {"application/x-zip-compressed": {}},
    "description": "Return a zip containing successfully converted files and log file"}

pdf_responses = dict(error_responses)
pdf_responses['200'] = {
    "content": {"application/pdf": {}},
    "description": "Return a graphical log of AGS data in .PDF format"}

ags_export_responses = dict(error_responses)
ags_export_responses['200'] = {
    "content": {"application/x-zip-compressed": {}, "application/json": {}},
    "description": ("Return a zip containing .ags file and metadata .txt file "
                    "or a json response containing the borehole ID count")}


checker_functions = {
    Checker.ags: check_ags,
    Checker.bgs: check_bgs,
}


@router.get("/ags_log/",
            tags=["ags_log"],
            summary="Generate Graphical Log",
            description=("Generate a graphical log (.pdf) from AGS data "
                         "held by the National Geoscience Data Centre."),
            response_class=Response,
            responses=pdf_responses)
def get_ags_log(bgs_loca_id: str = ags_log_query,
                response_type: ResponseType = response_type_query):
    """
    Get a graphical log (.pdf) for a single borehole in AGS format from the National Geoscience Data Centre.
    :param bgs_loca_id: The unique identifier of the borehole to generate the log for.
    :type bgs_loca_id: str
    :param response_type: The type of response to return (e.g. 'attachment' to force download or 'inline' \
    to display in browser).
    :type response_type: ResponseType, optional
    :return: A response containing a .pdf file with the generated borehole log.
    :rtype: Response
    :raises HTTPException 404: If the specified borehole does not exist or is confidential.
    :raises HTTPException 500: If the borehole generator returns an error.
    :raises HTTPException 500: If the borehole generator could not be reached.
    """

    url = BOREHOLE_VIEWER_URL.format(bgs_loca_id=bgs_loca_id)

    try:
        response = requests.get(url, timeout=10)
    except (Timeout, ConnectionError):
        raise HTTPException(status_code=500,
                            detail="The borehole generator could not be reached.  Please try again later.")

    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail=f"Failed to retrieve borehole {bgs_loca_id}. "
                                "It may not exist or may be confidential")
        else:
            raise HTTPException(status_code=500,
                                detail="The borehole generator returned an error.")

    filename = f"{bgs_loca_id}_log.pdf"
    headers = {'Content-Disposition': f'{response_type.value}; filename="{filename}"'}

    return Response(response.content, headers=headers, media_type='application/pdf')
