import requests

from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

import shapely

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.model.schema import BoreholeCountResponse
from app.model.queries import polygon_query, count_only_query
from .ags_export import ags_export
from .utils import (
    get_request_url,
    ags_export_responses,
    BOREHOLE_INDEX_URL,
    BOREHOLE_EXPORT_LIMIT,
    BOREHOLE_EXPORT_URL,
    AGS_API_VERSION,
)

router = APIRouter()


@router.get(
    f"{AGS_API_VERSION}/ags_export_by_polygon/",
    tags=["ags_export_by_polygon"],
    summary="Export a number of boreholes in .ags format in a polygon",
    description=(
        "Export a number of boreholes in .ags format from AGS data "
        "held by the National Geoscience Data Centre, using a"
        " polygon using Well-Known-Text."
    ),
    response_model=BoreholeCountResponse,
    responses=ags_export_responses,
)
def ags_export_by_polygon(
    polygon: str = polygon_query,
    count_only: bool = count_only_query,
    request: Request = None,
):
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
        raise HTTPException(status_code=422, detail="Invalid polygon")

    url = BOREHOLE_INDEX_URL.format(polygon=polygon, borehole_export_limit=BOREHOLE_EXPORT_LIMIT)

    try:
        response = requests.get(url, timeout=10)
    except (Timeout, ConnectionError):
        raise HTTPException(
            status_code=500,
            detail="The borehole index could not be reached.  Please try again later.",
        )

    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Failed to retrieve boreholes for the given polygon",
            )
        else:
            raise HTTPException(
                status_code=500, detail="The borehole index returned an error."
            )

    collection = response.json()
    count = collection["numberMatched"]

    if count_only:
        response = prepare_count_response(request, count)
    else:
        if count == 0:
            raise HTTPException(
                status_code=422, detail="No boreholes found in the given polygon"
            )
        elif count > BOREHOLE_EXPORT_LIMIT:
            raise HTTPException(
                status_code=422,
                detail=f"More than {BOREHOLE_EXPORT_LIMIT} boreholes ({count}) "
                "found in the given polygon. Please try with a smaller polygon",
            )

        bgs_loca_ids = ";".join([f["id"] for f in collection["features"]])
        url = BOREHOLE_EXPORT_URL.format(bgs_loca_id=bgs_loca_ids)
        response = ags_export(bgs_loca_ids)

    return response


def prepare_count_response(request, count):
    """Package the data into a BoreholeCountResponse schema object"""
    response_data = {
        "msg": "Borehole count",
        "type": "success",
        "self": get_request_url(request),
        "count": count,
    }
    return BoreholeCountResponse(**response_data, media_type="application/json")
