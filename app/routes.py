import tempfile
import shutil
import requests

from enum import StrEnum
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Form, Request, UploadFile, Response
from fastapi.responses import FileResponse, StreamingResponse


from app import conversion, validation
from app.checkers import check_ags, check_bgs
from app.errors import error_responses, InvalidPayloadError
from app.schemas import ValidationResponse

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
    "description": "Return a AGS Borehole log in .PDF format"}

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
class Response_type(StrEnum):
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


@router.post("/validate/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate(background_tasks: BackgroundTasks,
                   files: List[UploadFile] = validation_file,
                   std_dictionary: Dictionary = dictionary_form,
                   checkers: List[Checker] = validate_form,
                   fmt: Format = format_form,
                   request: Request = None):
    if not files[0].filename or not checkers:
        raise InvalidPayloadError(request)

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
             response_class=StreamingResponse,
             responses=zip_responses)
async def convert(background_tasks: BackgroundTasks,
                  files: List[UploadFile] = conversion_file,
                  sort_tables: bool = sort_tables_form,
                  request: Request = None):
    if not files[0].filename:
        raise InvalidPayloadError(request)
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
             responses=pdf_responses)
async def get_ags_log(bgs_loca_id: int,
                      response_type: Response_type = Response_type.inline):
    url = f"https://webservices.bgs.ac.uk/GWBV/viewborehole?loca_id={bgs_loca_id}"
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{bgs_loca_id}_log.pdf"
        headers = {'Content-Disposition': f'{response_type.value}; filename="{filename}"'}
        return Response(response.content, headers=headers, media_type='application/pdf')
    else:
        return {"error": f"Failed to retrieve borehole {bgs_loca_id}"}
