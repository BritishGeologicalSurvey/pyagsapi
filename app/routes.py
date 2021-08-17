import tempfile

from pathlib import Path
from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app import ags


router = APIRouter()


@router.post("/validate/", response_class=FileResponse)
async def validate(file: UploadFile = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    logfile = ags.validate(local_ags_file, tmp_dir)
    return logfile


@router.post("/validatemany/", response_class=FileResponse)
async def validate_many(files: List[UploadFile] = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    full_logfile = tmp_dir / 'logfile.log'
    for file in files:
        contents = await file.read()
        local_ags_file = tmp_dir / file.filename
        local_ags_file.write_bytes(contents)
        logfile = ags.validate(local_ags_file, tmp_dir)
        with full_logfile.open('at') as f:
            f.write(logfile.read_text())
            f.write('=' * 80 + '\n')
    return full_logfile
