"""Functions to handle the AGS parser."""
import datetime as dt
from functools import reduce
import logging
from pathlib import Path
from typing import Tuple, Optional

import python_ags4
from python_ags4 import AGS4

from app.response_templates import PLAIN_TEXT_TEMPLATE


logger = logging.getLogger(__name__)

# Collect full paths of dictionaries installed alongside python_ags4
_dictionary_files = list(Path(python_ags4.__file__).parent.glob('Standard_dictionary*.ags'))
STANDARD_DICTIONARIES = {f.name: f.absolute() for f in _dictionary_files}


def validate(filename: Path, standard_AGS4_dictionary: Optional[str] = None) -> dict:
    """
    Validate filename (against optional dictionary) and respond in
    dictionary suitable for converting to JSON.

    :raises ValueError: Raised if dictionary provided is not available.
    """
    logger.info("Validate called for %", filename.name)

    # Prepare response with metadata
    response = _prepare_response_metadata(filename)

    # Select dictionary file if exists
    if standard_AGS4_dictionary:
        try:
            dictionary_file = STANDARD_DICTIONARIES[standard_AGS4_dictionary]
        except KeyError:
            msg = (f"{standard_AGS4_dictionary} not available.  "
                   f"Installed dictionaries: {STANDARD_DICTIONARIES.keys()}")
            raise ValueError(msg)
    else:
        dictionary_file = None

    # Return early if file is not .ags format
    if filename.suffix != '.ags':
        response['message'] = f"ERROR: {filename.name} is not .ags format"
        return response

    # Get error information from file
    try:
        errors = AGS4.check_file(filename, standard_AGS4_dictionary=dictionary_file)
        try:
            metadata = errors.pop('Metadata')  # This also removes it from returned errors
            dictionary = [d['desc'] for d in metadata
                          if d['line'] == 'Dictionary'][0]
        except KeyError:
            # 'Metadata' is not created for some files with errors
            dictionary = ''

        error_count = len(reduce(lambda total, current: total + current, errors.values(), []))
        if error_count > 0:
            message = f'{error_count} error(s) found in file!'
            valid = False
        else:
            message = 'All checks passed!'
            valid = True
    except UnicodeDecodeError as err:
        line_no = len(err.object[:err.end].split(b'\n'))
        description = err.reason
        errors = {'UnicodeDecodeError': [
                       {'line': line_no, 'group': '', 'desc': description}]}
        dictionary = ''
        message = 'Unable to open file.'
        valid = False

    # Add error info to response
    response['dictionary'] = dictionary
    response['errors'] = errors
    response['message'] = message
    response['valid'] = valid

    return response


def to_plain_text(response: dict) -> str:
    """Take JSON response from convert and render as plain text."""
    return PLAIN_TEXT_TEMPLATE.render(response)


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


def is_valid(filename: Path, standard_AGS4_dictionary: Optional[str] = None) -> bool:
    """
    Validate filename and parse returned log to determine if file is valid.
    """
    return validate(filename, standard_AGS4_dictionary=standard_AGS4_dictionary)['valid']


def _prepare_response_metadata(filename: Path) -> dict:
    """
    Prepare a dictionary containing metadata to include in the response.
    """
    try:
        filesize = filename.stat().st_size
    except FileNotFoundError:
        filesize = 0

    response = {'filename': filename.name,
                'filesize': filesize,
                'checker': f'python_ags4 v{python_ags4.__version__}',
                'time': dt.datetime.now(tz=dt.timezone.utc),
                # The following are usually overwritten
                'message': '',
                'dictionary': '',
                'errors': {},
                'valid': False}
    return response
