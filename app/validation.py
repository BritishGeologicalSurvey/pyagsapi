"""
The validate function calls checkers to validate files and combines the
results in the requested format.
"""
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
             checkers: List[Callable[[Path], dict]] = [check_ags],
             standard_AGS4_dictionary: Optional[str] = None) -> dict:
    """
    Validate filename (against optional dictionary) and respond in
    dictionary suitable for converting to JSON.

    :raises ValueError: Raised if dictionary provided is not available.
    """
    logger.info("Validate called for %s", filename.name)

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

    all_errors = {}
    all_checkers = []
    additional_metadata_responses = {'bgs': {}, 'ags': {}}
    # Don't process if file is not .ags format
    if filename.suffix.lower() != '.ags':
        all_errors.update(
            {'File read error': [
                {'line': '-', 'group': '', 'desc': f'{filename.name} is not an .ags file'}
            ]})
    else:
        # Run checkers to extract errors and other metadata
        for checker in checkers:
            # result is a dictionary with 'errors', 'checker' and other keys
            result: dict = checker(filename, standard_AGS4_dictionary=dictionary_file)

            # Extract 'common' data
            all_errors.update(result.pop('errors'))
            current_checker = result.pop('checker')
            all_checkers.append(current_checker)

            additional_metadata = result.pop('additional_metadata')
            if current_checker.startswith('bgs_rules'):
                additional_metadata_responses['bgs'] = additional_metadata
            else:
                additional_metadata_responses['ags'] = additional_metadata

            # Add remaining keys to response
            response.update(result)

    # Use BGS metadata where available, as it contains more data
    if additional_metadata_responses['bgs']:
        response['additional_metadata'] = additional_metadata_responses['bgs']
    else:
        response['additional_metadata'] = additional_metadata_responses['ags']

    error_count = len(reduce(lambda total, current: total + current, all_errors.values(), []))
    if error_count > 0:
        message = f'{error_count} error(s) found in file!'
        valid = False
    else:
        message = 'All checks passed!'
        valid = True

    response.update(errors=all_errors, message=message, valid=valid, checkers=all_checkers)

    return response


def to_plain_text(response: dict) -> str:
    """Take JSON response from convert and render as plain text."""
    return PLAIN_TEXT_TEMPLATE.render(response)


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
                'time': dt.datetime.now(tz=dt.timezone.utc),
                # The following are usually overwritten
                'message': '',
                'dictionary': '',
                'errors': {},
                'checkers': [],
                'valid': True,
                'additional_metadata': {}}
    return response
