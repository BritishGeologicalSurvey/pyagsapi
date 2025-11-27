import requests

from fastapi import APIRouter, Response
from fastapi.exceptions import HTTPException

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app.model.schema import ResponseType
from app.model.queries import ags_log_query, response_type_query
from .utils import pdf_responses, BOREHOLE_VIEWER_URL, AGS_API_VERSION

router = APIRouter()


@router.get(
    f"{AGS_API_VERSION}/ags_log/",
    tags=["ags_log"],
    summary="Generate Graphical Log",
    description=(
        "Generate a graphical log (.pdf) from AGS data "
        "held by the National Geoscience Data Centre."
    ),
    response_class=Response,
    responses=pdf_responses,
)
def get_ags_log(
    bgs_loca_id: str = ags_log_query, response_type: ResponseType = response_type_query
):
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
        raise HTTPException(
            status_code=500,
            detail="The borehole generator could not be reached.  Please try again later.",
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
                status_code=500, detail="The borehole generator returned an error."
            )

    filename = f"{bgs_loca_id}_log.pdf"
    headers = {"Content-Disposition": f'{response_type.value}; filename="{filename}"'}

    return Response(response.content, headers=headers, media_type="application/pdf")
