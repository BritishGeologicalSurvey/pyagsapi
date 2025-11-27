import requests

from fastapi import APIRouter, Response
from fastapi.exceptions import HTTPException

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.model.queries import ags_export_query
from .utils import (
    ags_export_responses,
    BOREHOLE_EXPORT_LIMIT,
    BOREHOLE_EXPORT_URL,
    AGS_API_VERSION,
)

router = APIRouter()


@router.get(
    f"{AGS_API_VERSION}/ags_export/",
    tags=["ags_export"],
    summary="Export one or more boreholes in .ags format",
    description=(
        "Export one or more borehole in .ags format from AGS data "
        "held by the National Geoscience Data Centre."
    ),
    response_class=Response,
    responses=ags_export_responses,
)
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

    if len(bgs_loca_id.split(";")) > BOREHOLE_EXPORT_LIMIT:
        raise HTTPException(
            status_code=422, detail=f"More than {BOREHOLE_EXPORT_LIMIT} borehole IDs."
        )

    url = BOREHOLE_EXPORT_URL.format(bgs_loca_id=bgs_loca_id)

    try:
        response = requests.get(url, timeout=10)
    except (Timeout, ConnectionError):
        raise HTTPException(
            status_code=500,
            detail="The borehole exporter could not be reached.  Please try again later.",
        )

    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Failed to retrieve borehole {bgs_loca_id}. "
                "It may not exist or may be confidential",
            )
        else:
            raise HTTPException(
                status_code=500, detail="The borehole exporter returned an error."
            )

    headers = {"Content-Disposition": 'attachment; filename="boreholes.zip"'}

    return Response(
        response.content, headers=headers, media_type="application/x-zip-compressed"
    )
