"""Functions to handle the AGS parser."""
import datetime as dt
from functools import reduce
import logging
from pathlib import Path
import re
import subprocess
from typing import Tuple, Optional

import python_ags4
from python_ags4 import AGS4


from app.response_templates import PLAIN_TEXT_TEMPLATE, RESPONSE_TEMPLATE

logger = logging.getLogger(__name__)

# Collect full paths of dictionaries installed alongside python_ags4
_dictionary_files = list(Path(python_ags4.__file__).parent.glob('Standard_dictionary*.ags'))
STANDARD_DICTIONARIES = {f.name: f.absolute() for f in _dictionary_files}

logger = logging.getLogger(__name__)


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

        error_count = len(reduce(lambda acc, current: acc + current, errors.values(), []))
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
    if filename.suffix == '.ags':
        AGS4.AGS4_to_excel(filename, converted_file)
        message = f"SUCCESS: {filename.name} converted to {converted_file.name}"
    elif filename.suffix == '.xlsx':
        AGS4.excel_to_AGS4(filename, converted_file)
        message = f"SUCCESS: {filename.name} converted to {converted_file.name}"
    else:
        message = f"ERROR: {filename.name} is not .ags or .xlsx format"

    # Generate response based on result of subprocess
    #filesize = filename.stat().st_size / 1024
    #if result.returncode != 0:
    #    message = 'ERROR: ' + result.stderr
    #    converted_file.unlink(missing_ok=True)
    #    converted_file = None
    #elif result.stdout.startswith('ERROR: '):
    #    message = result.stdout
    #    converted_file.unlink(missing_ok=True)
    #    converted_file = None
    #else:
    #    message = f"SUCCESS: {filename.name} converted to {converted_file.name}"

    response['message'] = message

    return (converted_file, response)


def is_valid(filename: Path, standard_AGS4_dictionary: Optional[str] = None) -> bool:
    """
    Validate filename and parse returned log to determine if file is valid.
    """
    return validate(filename, standard_AGS4_dictionary=standard_AGS4_dictionary)['valid']


def get_unicode_message(stderr: str, filename: str) -> str:
    """
    Generate useful message from Unicode error
    """
    m = re.search(r'.*in position (\d+):.*', stderr)
    char_no, line_no, line, char = line_of_error(filename, int(m.group(1)))
    message = f'ERROR: Unreadable character "{char}" at position {char_no} on line: {line_no}\nStarting: {line}\n\n'
    return message


def line_of_error(filename: Path, char_no: int) -> Tuple[int, int, str, str]:
    """
    Return character, line number and start of line containing character at char_no.
    Also return problem character
    """
    with open(filename, encoding='ISO-8859-1') as f:
        upto = f.read(char_no)
        line_no = upto.count('\n') + 1
        line = upto.split('\n')[-1]
        char_no = len(line) + 1
        char = f.read(1)
    return char_no, line_no, line, char


def _prepare_response_metadata(filename: Path) -> dict:
    """
    Prepare a dictionary containing metadata to include in the response.
    """
    response = {'filename': filename.name,
                'filesize': filename.stat().st_size,
                'checker': f'python_ags4 v{python_ags4.__version__}',
                'dictionary': '',  # This is usually overwritten
                'time': dt.datetime.now(tz=dt.timezone.utc)}
    return response


class Ags4CliError(Exception):
    """Class for exceptions resulting from ags4_cli call."""
    pass
