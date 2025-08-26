import requests

from fastapi import APIRouter, Request, Response
from fastapi.exceptions import HTTPException

import shapely

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.checkers import check_ags, check_bgs
from app.errors import error_responses
from app.model.schema import Checker, ResponseType, BoreholeCountResponse
from app.model.queries import (ags_log_query, ags_export_query,
                               polygon_query, count_only_query, response_type_query)
from . utils import get_request_url

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


@router.get("/ags_export_by_polygon/",
            tags=["ags_export_by_polygon"],
            summary="Export a number of boreholes in .ags format in a polygon",
            description=("Export a number of boreholes in .ags format from AGS data "
                         "held by the National Geoscience Data Centre, using a"
                         " polygon using Well-Known-Text."),
            response_model=BoreholeCountResponse,
            responses=ags_export_responses)
def ags_export_by_polygon(polygon: str = polygon_query,
                          count_only: bool = count_only_query,
                          request: Request = None):
    """
    Export the boreholes in .ags format from AGS data held by the National Geoscience Data Centre,
    that are bounded by the polygon. If there are more than 50 boreholes return an error
    :param polygon: A polygon in Well Known Text.
    :type polygon: str
    :param count_only: The format to return the validation results in. Options are "text" or "json".
    :type count_only: int
    :param request: The request object.
    :type request: Request
    :return: A response with the validation results in either plain text or JSON format.
    :rtype: Union[BoreholeCountResponse, Response]
    :return: A response containing a count or a .zip file with the exported borehole data.
    :rtype: Response
    :raises HTTPException 422: If there are no boreholes or more than BOREHOLE_EXPORT_LIMIT boreholes in the polygon.
    :raises HTTPException 422: If the Well Known Text is not a POLYGON or is invalid.
    :raises HTTPException 500: If the borehole index could not be reached.
    :raises HTTPException 500: If the borehole index returns an error.
    :raises HTTPException 500: If the borehole exporter could not be reached.
    :raises HTTPException 500: If the borehole exporter returns an error.
    """

    # Check explicitly that the WKT is a valid POLYGON
    # The BOREHOLE_INDEX_URL API does not return an error for some bad WKT
    try:
        shapely.wkt.loads(polygon)
    except shapely.errors.GEOSException:
        raise HTTPException(status_code=422,
                            detail="Invalid polygon")

    url = BOREHOLE_INDEX_URL.format(polygon=polygon)

    try:
        response = requests.get(url, timeout=10)
    except (Timeout, ConnectionError):
        raise HTTPException(status_code=500,
                            detail="The borehole index could not be reached.  Please try again later.")

    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            raise HTTPException(status_code=404,
                                detail="Failed to retrieve boreholes for the given polygon")
        else:
            raise HTTPException(status_code=500,
                                detail="The borehole index returned an error.")

    collection = response.json()
    count = collection['numberMatched']

    if count_only:
        response = prepare_count_response(request, count)
    else:
        if count == 0:
            raise HTTPException(status_code=422,
                                detail="No boreholes found in the given polygon")
        elif count > BOREHOLE_EXPORT_LIMIT:
            raise HTTPException(status_code=422,
                                detail=f"More than {BOREHOLE_EXPORT_LIMIT} boreholes ({count}) "
                                "found in the given polygon. Please try with a smaller polygon")

        bgs_loca_ids = ';'.join([f['id'] for f in collection['features']])
        url = BOREHOLE_EXPORT_URL.format(bgs_loca_id=bgs_loca_ids)
        response = ags_export(bgs_loca_ids)

    return response


def prepare_count_response(request, count):
    """Package the data into a BoreholeCountResponse schema object"""
    response_data = {
        'msg': 'Borehole count',
        'type': 'success',
        'self': get_request_url(request),
        'count': count
    }
    return BoreholeCountResponse(**response_data, media_type="application/json")
