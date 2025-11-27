import tempfile
import shutil

from io import BytesIO
from pathlib import Path
from typing import List
from zipfile import is_zipfile, ZipFile

from fastapi import APIRouter, BackgroundTasks, Request, UploadFile
from fastapi.responses import StreamingResponse

from app import conversion, validation
from app.model.schema import SortingStrategy
from app.model.queries import sort_tables_form, conversion_file
from .errors import InvalidPayloadError
from .utils import AGS_API_VERSION, zip_responses

router = APIRouter()


@router.post(
    f"{AGS_API_VERSION}/convert/",
    tags=["convert"],
    response_class=StreamingResponse,
    responses=zip_responses,
    summary="Convert files between .ags and .xlsx format",
    description=(
        "Convert files between .ags and .xlsx format. "
        "Zipped files can be uploaded containing either filetype. "
        "Option to sort worksheets in .xlsx file in alphabetical order."
    ),
)
async def convert(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = conversion_file,
    sort_tables: str = sort_tables_form,
    request: Request = None,
):
    """
    Convert files between .ags and .xlsx format. Option to sort worksheets in .xlsx file in alphabetical order.
    :param background_tasks: A background task that manages file conversion asynchronously.
    :type background_tasks: BackgroundTasks
    :param files: A list of files to be converted. Must be in .ags, .xlsx or .zip format.
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
    RESULTS = "results"
    tmp_dir = Path(tempfile.mkdtemp())
    results_dir = tmp_dir / RESULTS
    results_dir.mkdir()
    full_logfile = results_dir / "conversion.log"
    with full_logfile.open("wt") as f:
        f.write("=" * 80 + "\n")
        for file in files:
            contents = await file.read()
            content_bytes = BytesIO(contents)
            # Extract zipped files if a zip is uploaded
            if is_zipfile(content_bytes) and not file.filename.lower().endswith(
                ".xlsx"
            ):
                zipfile = ZipFile(content_bytes)
                for name in zipfile.namelist():
                    zipfile.extract(name, tmp_dir)
                    local_file = tmp_dir / name
                    _, result = conversion.convert(
                        local_file, results_dir, sorting_strategy=sort_tables
                    )
                    log = validation.to_plain_text(result)
                    f.write(log)
                    f.write("\n" + "=" * 80 + "\n")
            else:
                local_file = tmp_dir / file.filename
                local_file.write_bytes(contents)
                _, result = conversion.convert(
                    local_file, results_dir, sorting_strategy=sort_tables
                )
                log = validation.to_plain_text(result)
                f.write(log)
                f.write("\n" + "=" * 80 + "\n")
    zipped_file = tmp_dir / RESULTS
    shutil.make_archive(zipped_file, "zip", results_dir)
    zipped_stream = open(tmp_dir / (RESULTS + ".zip"), "rb")

    background_tasks.add_task(zipped_stream.close)
    background_tasks.add_task(shutil.rmtree, tmp_dir)

    response = StreamingResponse(
        zipped_stream, media_type="application/x-zip-compressed"
    )
    response.headers["Content-Disposition"] = f"attachment; filename={RESULTS}.zip"
    return response
