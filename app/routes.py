import tempfile
import shutil

from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

from app import ags


router = APIRouter()


@router.post("/validate/", response_class=FileResponse)
async def validate(background_tasks: BackgroundTasks,
                   file: UploadFile = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    logfile = ags.validate(local_ags_file, tmp_dir)
    return logfile


@router.post("/validatemany/", response_class=FileResponse)
async def validate_many(background_tasks: BackgroundTasks,
                        files: List[UploadFile] = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)
    full_logfile = tmp_dir / 'logfile.log'
    with full_logfile.open('wt') as f:
        for file in files:
            contents = await file.read()
            local_ags_file = tmp_dir / file.filename
            local_ags_file.write_bytes(contents)
            logfile = ags.validate(local_ags_file, tmp_dir)
            f.write(logfile.read_text())
            f.write('=' * 80 + '\n')
    return full_logfile


@router.post("/convert/", response_class=StreamingResponse)
async def convert_many(background_tasks: BackgroundTasks,
                       files: List[UploadFile] = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    results_dir = tmp_dir / 'results'
    results_dir.mkdir()
    full_logfile = results_dir / 'conversion.log'
    with full_logfile.open('wt') as f:
        for file in files:
            contents = await file.read()
            local_file = tmp_dir / file.filename
            local_file.write_bytes(contents)
            converted, logfile = ags.convert(local_file, tmp_dir)
            if converted:
                converted_file = results_dir / converted.name
                converted_file.write_bytes(converted.read_bytes())
            f.write(logfile.read_text())
            f.write('=' * 80 + '\n')
    zipped_file = tmp_dir / 'results'
    shutil.make_archive(zipped_file, 'zip', results_dir)
    zipped_stream = open(tmp_dir / 'results.zip', 'rb')

    background_tasks.add_task(zipped_stream.close)
    background_tasks.add_task(shutil.rmtree, tmp_dir)

    response = StreamingResponse(zipped_stream, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=results.zip"
    return response
