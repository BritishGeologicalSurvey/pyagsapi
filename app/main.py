from typing import List

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request}) 

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


  
                                                                                                         
