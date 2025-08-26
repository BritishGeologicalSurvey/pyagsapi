import tempfile
import shutil

from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, Request, UploadFile
from fastapi.responses import StreamingResponse

from app import conversion, validation
from app.checkers import check_ags, check_bgs
from app.errors import error_responses, InvalidPayloadError
from app.model.schema import Checker, SortingStrategy
from app.model.queries import sort_tables_form, conversion_file

BOREHOLE_EXPORT_LIMIT = 50
BOREHOLE_VIEWER_URL = "https://gwbv.bgs.ac.uk/GWBV/viewborehole?loca_id={bgs_loca_id}"
BOREHOLE_EXPORT_URL = "https://gwbv.bgs.ac.uk/ags_export?loca_ids={bgs_loca_id}"
BOREHOLE_INDEX_URL = ("https://ogcapi.bgs.ac.uk/collections/agsboreholeindex/items?f=json"
                      "&properties=bgs_loca_id&filter=INTERSECTS(shape,{polygon})&limit=10")

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
    "description": "Return a graphical log of AGS data in .PDF format"}

ags_export_responses = dict(error_responses)
ags_export_responses['200'] = {
    "content": {"application/x-zip-compressed": {}, "application/json": {}},
    "description": ("Return a zip containing .ags file and metadata .txt file "
                    "or a json response containing the borehole ID count")}


checker_functions = {
    Checker.ags: check_ags,
    Checker.bgs: check_bgs,
}


@router.post("/convert/",
             tags=["convert"],
             response_class=StreamingResponse,
             responses=zip_responses,
             summary="Convert files between .ags and .xlsx format",
             description=("Convert files between .ags and .xlsx format. Option to"
                          " sort worksheets in .xlsx file in alphabetical order."))
async def convert(background_tasks: BackgroundTasks,
                  files: List[UploadFile] = conversion_file,
                  sort_tables: str = sort_tables_form,
                  request: Request = None):
    """
    Convert files between .ags and .xlsx format. Option to sort worksheets in .xlsx file in alphabetical order.
    :param background_tasks: A background task that manages file conversion asynchronously.
    :type background_tasks: BackgroundTasks
    :param files: A list of files to be converted. Must be in .ags or .xlsx format.
    :type files: List[UploadFile]
    :param sort_tables: A boolean indicating whether to sort worksheets in the .xlsx file in alphabetical order.
    :type sort_tables: bool
    :param request: The HTTP request object.
    :type request: Request
    :return: A streaming response containing a .zip file with the converted files and a log file.
    :rtype: StreamingResponse
    :raises InvalidPayloadError: If the request payload is invalid.
    :raises Exception: If the conversion fails or an unexpected error occurs.
    """

    if sort_tables == SortingStrategy.default:
        sort_tables = None
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
            _, result = conversion.convert(local_file, results_dir, sorting_strategy=sort_tables)
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
