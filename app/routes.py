import tempfile
import shutil
import requests

from enum import StrEnum
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Form, Query, Request, UploadFile, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.exceptions import HTTPException

from requests.exceptions import Timeout, ConnectionError, HTTPError

from app import conversion, validation
from app.checkers import check_ags, check_bgs
from app.errors import error_responses, InvalidPayloadError
from app.schemas import ValidationResponse

BOREHOLE_VIEWER_URL = "https://gwbv.bgs.ac.uk/GWBV/viewborehole?loca_id={bgs_loca_id}"
BOREHOLE_EXPORT_URL = "https://gwbv.bgs.ac.uk/ags_export/"

router = APIRouter()

log_responses = dict(error_responses)
log_responses['200'] = {
    "content": {"application/json": {}, "text/plain": {}},
    "description": "Return a log in json or text"}

zip_responses = dict(error_responses)
zip_responses['200'] = {
    "content": {"application/x-zip-compressed": {}},
    "description": "Return a zip containing successfully converted files and log file"}

zip_ags_responses = dict(error_responses)
zip_ags_responses['200'] = {
    "content": {"application/x-zip-compressed": {}},
    "description": "Return a zip containing .ags file and metadata .txt file"}

pdf_responses = dict(error_responses)
pdf_responses['200'] = {
    "content": {"application/pdf": {}},
    "description": "Return a graphical log of AGS data in .PDF format"}


# Enum for search logic
class Format(StrEnum):
    TEXT = "text"
    JSON = "json"


# Enum for search logic
class Dictionary(StrEnum):
    v4_0_3 = "v4_0_3"
    v4_0_4 = "v4_0_4"
    v4_1 = "v4_1"
    v4_1_1 = "v4_1_1"


# Enum for checker logic
class Checker(StrEnum):
    ags = "ags"
    bgs = "bgs"


# Enum for pdf response type logic
class ResponseType(StrEnum):
    attachment = "attachment"
    inline = "inline"


checker_functions = {
    Checker.ags: check_ags,
    Checker.bgs: check_bgs,
}

format_form = Form(
    default=Format.JSON,
    title='Response Format',
    description='Response format: json or text',
)

dictionary_form = Form(
    default=None,
    title='Validation Dictionary',
    description='Version of AGS dictionary to validate against',
)

validate_form = Form(
    default=None,
    title='Validation Options',
    description='If set validate against AGS schema',
)

validation_file = File(
    ...,
    title='File to validate',
    description='An AGS file ending in .ags',
)

conversion_file = File(
    ...,
    title='File to convert',
    description='An AGS or XLSX file',
)

sort_tables_form = Form(
    default=False,
    title='Sort worksheets',
    description=('Sort the worksheets into alphabetical order '
                 'or leave in the order found in the AGS file. '
                 'This option is ignored when converting to AGS.'),
)

ags_log_query = Query(
    ...,
    title="BGS LOCA ID",
    description="BGS LOCA ID",
    example="20190430093402523419",
)

ags_export_query = Query(
    ...,
    title="BGS LOCA ID",
    description="BGS LOCA ID",
    example="20190430093402523419",
)

response_type_query = Query(
    default=ResponseType.inline,
    title='PDF Response Type',
    description='PDF response type: inline or attachment',
)


@router.post("/validate/",
             tags=["validate"],
             response_model=ValidationResponse,
             responses=log_responses,
             summary="Validate AGS4 File(s)",
             description=("Validate an AGS4 file to the AGS File Format v4.x rules and the NGDC data"
                          " submission requirements. Uses the Offical AGS4 Python Library."))
async def validate(background_tasks: BackgroundTasks,
                   files: List[UploadFile] = validation_file,
                   std_dictionary: Dictionary = dictionary_form,
                   checkers: List[Checker] = validate_form,
                   fmt: Format = format_form,
                   request: Request = None):
    if not files[0].filename or not checkers:
        raise InvalidPayloadError(request)
    """
    Validate an AGS4 file to the AGS File Format v4.x rules and the NGDC data submission requirements.
    Uses the Official AGS4 Python Library.

    :param background_tasks: Background tasks for deleting temporary directories.
    :type background_tasks: BackgroundTasks

    :param files: List of AGS4 files to be validated.
    :type files: List[UploadFile]

    :param std_dictionary: The standard dictionary to use for validation. Options are "BGS" or "AGS".
    :type std_dictionary: Dictionary

    :param checkers: List of validation rules to be used during validation.
    :type checkers: List[Checker]

    :param fmt: The format to return the validation results in. Options are "text" or "json".
    :type fmt: Format

    :param request: The request object.
    :type request: Request

    :return: A response with the validation results in either plain text or JSON format.
    :rtype: Union[FileResponse, ValidationResponse]

    :raises InvalidPayloadError: If the payload is missing files or checkers.
    """
    checkers = [checker_functions[c] for c in checkers]

    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    dictionary = None
    if std_dictionary:
        dictionary = f'Standard_dictionary_{std_dictionary}.ags'

    data = []
    for file in files:
        contents = await file.read()
        local_ags_file = tmp_dir / file.filename
        local_ags_file.write_bytes(contents)
        result = validation.validate(
            local_ags_file, checkers=checkers, standard_AGS4_dictionary=dictionary)
        data.append(result)

    if fmt == Format.TEXT:
        full_logfile = tmp_dir / 'results.log'
        with full_logfile.open('wt') as f:
            f.write('=' * 80 + '\n')
            for result in data:
                log = validation.to_plain_text(result)
                f.write(log)
                f.write('=' * 80 + '\n')
        response = FileResponse(full_logfile, media_type="text/plain")
    else:
        response = prepare_validation_response(request, data)

    return response


@router.post("/convert/",
             tags=["convert"],
             response_class=StreamingResponse,
             responses=zip_responses,
             summary="Convert files between .ags and .xlsx format",
             description=("Convert files between .ags and .xlsx format. Option to"
                          " sort worksheets in .xlsx file in alphabetical order."))
async def convert(background_tasks: BackgroundTasks,
                  files: List[UploadFile] = conversion_file,
                  sort_tables: bool = sort_tables_form,
                  request: Request = None):
    if not files[0].filename:
        raise InvalidPayloadError(request)
    """
    Convert files between .ags and .xlsx format. Option to sort worksheets in .xlsx file in alphabetical order.

    :param background_tasks: A background task that manages file conversion asynchronously.
    :type background_tasks: BackgroundTasks

    :param files: A list of files to be converted. Must be in .ags or .xlsx format.
    :type files: List[UploadFile]

    :param sort_tables: A boolean indicating whether to sort worksheets in the .xlsx file in alphabetical order.
    :type sort_tables: bool

    :param request: The HTTP request object.
    :type request: Request

    :return: A streaming response containing a .zip file with the converted files and a log file.
    :rtype: StreamingResponse

    :raises InvalidPayloadError: If the request payload is invalid.
    :raises Exception: If the conversion fails or an unexpected error occurs.
    """
    RESULTS = 'results'
    tmp_dir = Path(tempfile.mkdtemp())
    results_dir = tmp_dir / RESULTS
    results_dir.mkdir()
    full_logfile = results_dir / 'conversion.log'
    with full_logfile.open('wt') as f:
        f.write('=' * 80 + '\n')
        for file in files:
            contents = await file.read()
            local_file = tmp_dir / file.filename
            local_file.write_bytes(contents)
            converted, result = conversion.convert(local_file, results_dir, sort_tables=sort_tables)
            log = validation.to_plain_text(result)
            f.write(log)
            f.write('\n' + '=' * 80 + '\n')
    zipped_file = tmp_dir / RESULTS
    shutil.make_archive(zipped_file, 'zip', results_dir)
    zipped_stream = open(tmp_dir / (RESULTS + '.zip'), 'rb')

    background_tasks.add_task(zipped_stream.close)
    background_tasks.add_task(shutil.rmtree, tmp_dir)

    response = StreamingResponse(zipped_stream, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={RESULTS}.zip"
    return response


def prepare_validation_response(request, data):
    """Package the data into a Response schema object"""
    response_data = {
        'msg': f'{len(data)} files validated',
        'type': 'success',
        'self': str(request.url),
        'data': data,
    }
    return ValidationResponse(**response_data, media_type="application/json")


@router.get("/ags_log/",
            tags=["ags_log"],
            summary="Generate Graphical Log",
            description="Generate a graphical log (.pdf) from AGS data held by the National Geoscience Data Centre.",
            include_in_schema=True,
            response_class=Response,
            responses=pdf_responses)
def get_ags_log(bgs_loca_id: int = ags_log_query,
                response_type: ResponseType = response_type_query):
    """
    Get a graphical log (.pdf) for a single borehole in AGS format from the National Geoscience Data Centre.

    :param bgs_loca_id: The unique identifier of the borehole to generate the log for.
    :type bgs_loca_id: int

    :param response_type: The type of response to return (e.g. 'attachment' to force download or 'inline' \
    to display in browser).
    :type response_type: ResponseType, optional

    :return: A response containing a .pdf file with the generated borehole log.
    :rtype: Response

    :raises HTTPException 500: If the borehole generator could not be reached.
    :raises HTTPException 404: If the specified borehole does not exist or is confidential.
    :raises HTTPException 500: If the borehole generator returns an error.

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


@router.post("/ags_export/",
             tags=["ags_export"],
             summary="Export a single borehole in .ags format",
             description="Export a single borehole in .ags format from AGS data \
             held by the National Geoscience Data Centre.",
             include_in_schema=True,
             response_class=StreamingResponse,
             responses=zip_ags_responses)
def post_ags_export(bgs_loca_id: int = ags_export_query):
    """
    Export a single borehole in .ags format from AGS data held by the National Geoscience Data Centre.

    :param bgs_loca_id: The unique identifier of the borehole to export.
    :type bgs_loca_id: int

    :return: A streaming response containing a .zip file with the exported borehole data.
    :rtype: StreamingResponse

    :raises HTTPException 500: If the borehole exporter could not be reached.
    :raises HTTPException 404: If the specified borehole does not exist or is confidential.
    :raises HTTPException 500: If the borehole exporter returns an error.
    """
    url = BOREHOLE_EXPORT_URL
    data = str(bgs_loca_id)
    headers = {"Content-Type": "text/plain",
               "Accept": "*/*",
               "Accept-Encoding": "gzip, deflate, br",
               "Connection": "keep-alive"}

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
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

    content = response.content
    response = StreamingResponse(content, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = f"attachment; filename={bgs_loca_id}.zip"
    return response
