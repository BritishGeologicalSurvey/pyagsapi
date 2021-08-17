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


@router.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}
