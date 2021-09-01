"""Validation function and helpers"""
import datetime as dt
from functools import reduce
import logging
from pathlib import Path
from typing import Optional, Callable, List

import python_ags4

from app.checkers import check_ags
from app.response_templates import PLAIN_TEXT_TEMPLATE

logger = logging.getLogger(__name__)

# Collect full paths of dictionaries installed alongside python_ags4
_dictionary_files = list(Path(python_ags4.__file__).parent.glob('Standard_dictionary*.ags'))
STANDARD_DICTIONARIES = {f.name: f.absolute() for f in _dictionary_files}


def validate(filename: Path,
             checkers: List[Callable[Path, dict]] = [check_ags],
             standard_AGS4_dictionary: Optional[str] = None) -> dict:
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
        response['valid'] = False
        return response

    # Run checkers to extract errors and other metadata
    all_errors = {}
    for checker in checkers:
        # Result is a dictionary with 'errors' and other keys
        result = checker(filename, standard_AGS4_dictionary=dictionary_file)
        # Pull 'errors' out to add to running total
        all_errors.update(result.pop('errors'))
        # Add remaining keys to response
        response.update(result)

    error_count = len(reduce(lambda total, current: total + current, all_errors.values(), []))
    if error_count > 0:
        message = f'{error_count} error(s) found in file!'
        valid = False
    else:
        message = 'All checks passed!'
        valid = True

    response.update(errors=all_errors, message=message, valid=valid)

    return response


def to_plain_text(response: dict) -> str:
    """Take JSON response from convert and render as plain text."""
    return PLAIN_TEXT_TEMPLATE.render(response)


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
                'valid': True}
    return response
