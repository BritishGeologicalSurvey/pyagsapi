from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/check/")
async def check(files: List[bytes] = File(...)):
    # Create temp dir
    # Loop over files
    #   - save to temp dir
    #   - call validate (and save log)
    # Zip up log files
    # Return zip
    # Errors should be 4xx if invalid file is uploaded
    return {"file_sizes": [len(file) for file in files]}


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
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
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
