import tempfile
import shutil

from pathlib import Path
from typing import List

from fastapi import APIRouter, BackgroundTasks, Request, UploadFile
from fastapi.responses import FileResponse

from app import validation
from app.borehole_map import extract_geojson
from app.checkers import check_ags, check_bgs
from app.errors import error_responses, InvalidPayloadError
from app.model.schema import Checker, Format, Dictionary, ValidationResponse
from app.model.queries import (format_form, geometry_form, dictionary_form, validate_form,
                               validation_file)
from . utils import get_request_url

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


@router.post("/validate/",
             tags=["validate"],
             response_model=ValidationResponse,
             responses=log_responses,
             summary="Validate AGS4 File(s)",
             description=("Validate an AGS4 file to the AGS File Format v4.x rules and the NGDC data"
                          " submission requirements. Uses the Offical AGS4 Python Library."))
async def validate(background_tasks: BackgroundTasks,
                   files: List[UploadFile] = validation_file,
                   std_dictionary: Dictionary = dictionary_form,
                   checkers: List[Checker] = validate_form,
                   fmt: Format = format_form,
                   return_geometry: bool = geometry_form,
                   request: Request = None):
    """
    Validate an AGS4 file to the AGS File Format v4.x rules and the NGDC data submission requirements.
    Uses the Official AGS4 Python Library.
    :param background_tasks: Background tasks for deleting temporary directories.
    :type background_tasks: BackgroundTasks
    :param files: List of AGS4 files to be validated.
    :type files: List[UploadFile]
    :param std_dictionary: The standard dictionary to use for validation. Options are "BGS" or "AGS".
    :type std_dictionary: Dictionary
    :param checkers: List of validation rules to be used during validation.
    :type checkers: List[Checker]

    :param fmt: The format to return the validation results in. Options are "text" or "json".
    :type fmt: Format
    :param return_geometry: Include GeoJSON in validation response. Options are True or False.
    :type return_geometry: bool
    :param request: The request object.
    :type request: Request
    :return: A response with the validation results in either plain text or JSON format.
    :rtype: Union[FileResponse, ValidationResponse]
    :raises InvalidPayloadError: If the payload is missing files or checkers.
    """

    if not files[0].filename or not checkers:
        raise InvalidPayloadError(request)

    checkers = [checker_functions[c] for c in checkers]

    tmp_dir = Path(tempfile.mkdtemp())
    background_tasks.add_task(shutil.rmtree, tmp_dir)

    if std_dictionary == Dictionary.None_Given:
        dictionary = None
    else:
        dictionary = f'Standard_dictionary_{std_dictionary}.ags'

    data = []
    for file in files:
        contents = await file.read()
        local_ags_file = tmp_dir / file.filename
        local_ags_file.write_bytes(contents)
        result = validation.validate(
            local_ags_file, checkers=checkers, standard_AGS4_dictionary=dictionary)
        if return_geometry:
            try:
                geojson = extract_geojson(local_ags_file)
                result['geojson'] = geojson
            except ValueError as ve:
                result['geojson'] = {}
                result['geojson_error'] = str(ve)
        data.append(result)

    if fmt == Format.TEXT:
        full_logfile = tmp_dir / 'results.log'
        with full_logfile.open('wt') as f:
            f.write('=' * 80 + '\n')
            for result in data:
                log = validation.to_plain_text(result)
                f.write(log)
                f.write('=' * 80 + '\n')
        response = FileResponse(full_logfile, media_type="text/plain")
    else:
        response = prepare_validation_response(request, data)

    return response


def prepare_validation_response(request, data):
    """Package the data into a Response schema object"""
    response_data = {
        'msg': f'{len(data)} files validated',
        'type': 'success',
        'self': get_request_url(request),
        'data': data,
    }
    return ValidationResponse(**response_data, media_type="application/json")
