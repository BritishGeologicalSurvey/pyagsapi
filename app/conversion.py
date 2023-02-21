import logging
from pathlib import Path
from typing import Tuple, Optional

from python_ags4 import AGS4

from app.validation import _prepare_response_metadata


logger = logging.getLogger(__name__)


def convert(filename: Path, results_dir: Path) -> Tuple[Optional[Path], dict]:
    """
    Convert filename between .ags and .xlsx.  Write output to file in
    results_dir and return path alongside job status data in dictionary."""
    # Prepare variables and directory
    new_extension = '.ags' if filename.suffix == '.xlsx' else '.xlsx'
    converted_file = results_dir / (filename.stem + new_extension)
    logger.info("Converting %s to %s", filename.name, converted_file.name)
    if not results_dir.exists():
        results_dir.mkdir()

    # Prepare response with metadata
    response = _prepare_response_metadata(filename)

    # Do the conversion
    success = False
    if filename.suffix == '.ags':
        try:
            AGS4.AGS4_to_excel(filename, converted_file)
            success = True
        except IndexError:
            error_message = "ERROR: File does not have AGS4 format layout"
        except UnboundLocalError:
            # This error is thrown in response to a bug in the upstream code,
            # which in turn is only triggered if the AGS file has duplicate
            # headers.
            error_message = "ERROR: File contains duplicate headers"
        except AGS4.AGS4Error as err:
            error_message = str(err)
    elif filename.suffix == '.xlsx':
        try:
            AGS4.excel_to_AGS4(filename, converted_file)
            if converted_file.exists():
                success = True
            else:
                # The underlying conversion fails silently,
                # the file does not then exist.
                # Propagate a short error message
                error_message = "ERROR: Conversion failed"
        except AttributeError as err:
            # Include error details here in case they provide a clue e.g. which
            # attribute is missing
            error_message = f"ERROR: Bad spreadsheet layout ({err.args[0]})"
    else:
        error_message = f"ERROR: {filename.name} is not .ags or .xlsx format"

    # Update response and clean failed files
    if success:
        response['message'] = f"SUCCESS: {filename.name} converted to {converted_file.name}"
        response['valid'] = True
    else:
        response['message'] = error_message
        response['valid'] = False
        converted_file.unlink(missing_ok=True)
        converted_file = None

    return (converted_file, response)
