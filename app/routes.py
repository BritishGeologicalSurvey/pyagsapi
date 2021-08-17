import tempfile
import shutil

from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, File, UploadFile
from fastapi.responses import FileResponse

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
