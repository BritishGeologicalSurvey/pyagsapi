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
    success = True
    if filename.suffix == '.ags':
        try:
            AGS4.AGS4_to_excel(filename, converted_file)
        except IndexError:
            success = False
            error_message = "ERROR: File does not have AGS4 format layout"
        except UnboundLocalError:
            # This error is thrown in response to a bug in the upstream code,
            # which in turn is only triggered if the AGS file has duplicate
            # headers.
            success = False
            error_message = "ERROR: File contains duplicate headers"
        except SystemExit:
            # There are two function calls in python_ags4.AGS4 that throw a
            # sys.exit in reponse to a bad file.  The associated errors are
            # summarised here.
            success = False
            error_message = "ERROR: UNIT and/or TYPE rows missing OR mismatched column numbers"
    elif filename.suffix == '.xlsx':
        try:
            AGS4.excel_to_AGS4(filename, converted_file)
        except AttributeError as err:
            # Include error details here in case they provide a clue e.g. which
            # attribute is missing
            success = False
            error_message = f"ERROR: Bad spreadsheet layout ({err.args[0]})"
    else:
        success = False
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
