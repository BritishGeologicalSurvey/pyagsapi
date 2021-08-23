import tempfile
import shutil

from enum import Enum
from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, Query, Request, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from app import ags
from app.errors import error_responses, InvalidPayloadError
from app.schemas import ValidationResponse

router = APIRouter()

log_responses = dict(error_responses)
log_responses['200'] = {
    "content": {"text/plain": {}},
    "description": "Return a log file"}

zip_responses = dict(error_responses)
zip_responses['200'] = {
    "content": {"application/x-zip-compressed": {}},
    "description": "Return a zip containing successfully converted files and log file"}


# Enum for search logic
class Format(str, Enum):
    TEXT = "text"
    JSON = "json"


format_query = Query(
    default=Format.JSON,
    title='Format',
    description='Response format, text or json',
)


@router.post("/isvalid/",
             response_model=ValidationResponse,
             responses=log_responses)
async def is_valid(background_tasks: BackgroundTasks,
                   file: UploadFile = File(...),
                   request: Request = None):
    if not file.filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    valid = ags.is_valid(local_ags_file)
    data = [valid]
    response = prepare_validation_response(request, data)
    return response


@router.post("/validate/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate(background_tasks: BackgroundTasks,
                   file: UploadFile = File(...),
                   fmt: Format = format_query,
                   request: Request = None):
    if not file.filename:
        raise InvalidPayloadError(request)
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    log = ags.validate(local_ags_file)
    if fmt == Format.TEXT:
        logfile = tmp_dir / 'results.log'
        logfile.write_text(log)
        response = FileResponse(logfile, media_type="text/plain")
    else:
        data = [log]
        response = prepare_validation_response(request, data)
    return response


@router.post("/validatemany/",
             response_model=ValidationResponse,
             responses=log_responses)
async def validate_many(background_tasks: BackgroundTasks,
                        files: List[UploadFile] = File(...),
                        fmt: Format = format_query,
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
                log = ags.validate(local_ags_file)
                f.write(log)
                f.write('=' * 80 + '\n')
        response = FileResponse(full_logfile, media_type="text/plain")
    else:
        data = []
        for file in files:
            contents = await file.read()
            local_ags_file = tmp_dir / file.filename
            local_ags_file.write_bytes(contents)
            log = ags.validate(local_ags_file)
            data.append(log)
        response = prepare_validation_response(request, data)
    return response


@router.post("/convert/",
             response_class=StreamingResponse,
             responses=zip_responses)
async def convert_many(background_tasks: BackgroundTasks,
                       files: List[UploadFile] = File(...),
                       fmt: Format = format_query,
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
            converted, log = ags.convert(local_file, results_dir)
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
    return ValidationResponse(**response_data)
