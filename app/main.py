import tempfile

from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

import ags


app = FastAPI()


@app.post("/validate/", response_class=FileResponse)
async def validate(file: UploadFile = File(...)):
    tmp_dir = Path(tempfile.mkdtemp())
    contents = await file.read()
    local_ags_file = tmp_dir / file.filename
    local_ags_file.write_bytes(contents)
    logfile = ags.validate(local_ags_file, tmp_dir)
    return logfile


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
<title>AGS File Validator</title>
</head>
<body>
<h1>AGS File Validator</h1>
<br>
<h2>AGS File Size</h2>
<form action="/validate/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
<br>
<h2>AGS File Name</h2>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
</html>
    """
    return HTMLResponse(content=content)
