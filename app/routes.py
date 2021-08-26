import tempfile
import shutil

from enum import Enum
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from app import ags, bgs
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


# Enum for search logic
class Format(str, Enum):
    TEXT = "text"
    JSON = "json"


# Enum for search logic
class Dictionary(str, Enum):
    V4_0_3 = "v4_0_3"
    V4_0_4 = "v4_0_4"
    V4_1 = "v4_1"


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


@router.post("/isvalid/",
             response_model=ValidationResponse,
             responses=log_responses)
async def is_valid(background_tasks: BackgroundTasks,
                   file: UploadFile = validation_file,
                   std_dictionary: Dictionary = dictionary_form,
                   request: Request = None):
    if not file.filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    dictionary = None
    if std_dictionary:
        dictionary = f'Standard_dictionary_{std_dictionary}.ags'
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    valid = ags.is_valid(local_ags_file, standard_AGS4_dictionary=dictionary)
    data = [valid]
    response = prepare_validation_response(request, data)
    return response


@router.post("/validate/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate(background_tasks: BackgroundTasks,
                   file: UploadFile = validation_file,
                   std_dictionary: Dictionary = dictionary_form,
                   fmt: Format = format_form,
                   request: Request = None):
    if not file.filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    dictionary = None
    if std_dictionary:
        dictionary = f'Standard_dictionary_{std_dictionary}.ags'
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    result = ags.validate(local_ags_file, standard_AGS4_dictionary=dictionary)
    if fmt == Format.TEXT:
        log = ags.to_plain_text(result)
        logfile = tmp_dir / 'results.log'
        logfile.write_text(log)
        response = FileResponse(logfile, media_type="text/plain")
    else:
        data = [result]
        response = prepare_validation_response(request, data)
    return response


@router.post("/validatemany/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate_many(background_tasks: BackgroundTasks,
                        files: List[UploadFile] = validation_file,
                        std_dictionary: Dictionary = dictionary_form,
                        fmt: Format = format_form,
                        request: Request = None):
    if not files[0].filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    dictionary = None
    if std_dictionary:
        dictionary = f'Standard_dictionary_{std_dictionary}.ags'
    if fmt == Format.TEXT:
        full_logfile = tmp_dir / 'results.log'
        with full_logfile.open('wt') as f:
            for file in files:
                contents = await file.read()
                local_ags_file = tmp_dir / file.filename
                local_ags_file.write_bytes(contents)
                result = ags.validate(local_ags_file, standard_AGS4_dictionary=dictionary)
                log = ags.to_plain_text(result)
                f.write(log)
                f.write('=' * 80 + '\n')
        response = FileResponse(full_logfile, media_type="text/plain")
    else:
        data = []
        for file in files:
            contents = await file.read()
            local_ags_file = tmp_dir / file.filename
            local_ags_file.write_bytes(contents)
            result = ags.validate(local_ags_file, standard_AGS4_dictionary=dictionary)
            data.append(result)
        response = prepare_validation_response(request, data)
    return response


@router.post("/convert/",
             response_class=StreamingResponse,
             responses=zip_responses)
async def convert_many(background_tasks: BackgroundTasks,
                       files: List[UploadFile] = conversion_file,
                       request: Request = None):
    if not files[0].filename:
        raise InvalidPayloadError(request)
    RESULTS = 'results'
    tmp_dir = Path(tempfile.mkdtemp())
    results_dir = tmp_dir / RESULTS
    results_dir.mkdir()
    full_logfile = results_dir / 'conversion.log'
    with full_logfile.open('wt') as f:
        for file in files:
            contents = await file.read()
            local_file = tmp_dir / file.filename
            local_file.write_bytes(contents)
            converted, result = ags.convert(local_file, results_dir)
            log = ags.to_plain_text(result)
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


@router.post("/validatedatamany/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate_data_many(background_tasks: BackgroundTasks,
                             files: List[UploadFile] = validation_file,
                             fmt: Format = format_form,
                             request: Request = None):
    if not files[0].filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    if fmt == Format.TEXT:
        full_logfile = tmp_dir / 'results.log'
        with full_logfile.open('wt') as f:
            for file in files:
                contents = await file.read()
                local_ags_file = tmp_dir / file.filename
                local_ags_file.write_bytes(contents)
                result = bgs.validate(local_ags_file)
                log = bgs.to_plain_text(result)
                f.write(log)
                f.write('=' * 80 + '\n')
        response = FileResponse(full_logfile, media_type="text/plain")
    else:
        data = []
        for file in files:
            contents = await file.read()
            local_ags_file = tmp_dir / file.filename
            local_ags_file.write_bytes(contents)
            result = bgs.validate(local_ags_file)
            data.append(result)
        response = prepare_validation_response(request, data)
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
