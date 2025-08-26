import requests

from fastapi import APIRouter, Response
from fastapi.exceptions import HTTPException

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.checkers import check_ags, check_bgs
from app.errors import error_responses
from app.model.schema import Checker
from app.model.queries import ags_export_query

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


@router.get("/ags_export/",
            tags=["ags_export"],
            summary="Export one or more boreholes in .ags format",
            description=("Export one or more borehole in .ags format from AGS data "
                         "held by the National Geoscience Data Centre."),
            response_class=Response,
            responses=ags_export_responses)
def ags_export(bgs_loca_id: str = ags_export_query):
    """
    Export a single borehole in .ags format from AGS data held by the National Geoscience Data Centre.
    :param bgs_loca_id: The unique identifier of the borehole to export.
    :type bgs_loca_id: str
    :return: A response containing a .zip file with the exported borehole data.
    :rtype: Response
    :raises HTTPException 404: If the specified boreholes do not exist or are confidential.
    :raises HTTPException 422: If more than BOREHOLE_EXPORT_LIMIT borehole IDs are supplied.
    :raises HTTPException 500: If the borehole exporter returns an error.
    :raises HTTPException 500: If the borehole exporter could not be reached.
    """

    if len(bgs_loca_id.split(';')) > BOREHOLE_EXPORT_LIMIT:
        raise HTTPException(status_code=422, detail=f"More than {BOREHOLE_EXPORT_LIMIT} borehole IDs.")

    url = BOREHOLE_EXPORT_URL.format(bgs_loca_id=bgs_loca_id)

    try:
        response = requests.get(url, timeout=10)
    except (Timeout, ConnectionError):
        raise HTTPException(status_code=500,
                            detail="The borehole exporter could not be reached.  Please try again later.")

    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail=f"Failed to retrieve borehole {bgs_loca_id}. "
                                "It may not exist or may be confidential")
        else:
            raise HTTPException(status_code=500,
                                detail="The borehole exporter returned an error.")

    headers = {'Content-Disposition': 'attachment; filename="boreholes.zip"'}

    return Response(response.content, headers=headers, media_type='application/x-zip-compressed')
