"""Functions to handle the AGS parser."""
import datetime as dt
from functools import reduce
import logging
from pathlib import Path

from python_ags4 import AGS4

from app.response_templates import PLAIN_TEXT_TEMPLATE


logger = logging.getLogger(__name__)


def validate(filename: Path) -> dict:
    """
    Validate filename against BGS criteria and respond in
    dictionary suitable for converting to JSON.
    """
    logger.info("BGS validate called for %", filename.name)

    # Prepare response with metadata
    response = _prepare_response_metadata(filename)

    # Return early if file is not .ags format
    if filename.suffix != '.ags':
        response['message'] = f"ERROR: {filename.name} is not .ags format"
        return response

    # Get error information from file
    try:
        errors = check_file(filename)
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
        message = 'Unable to open file.'
        valid = False

    # Add error info to response
    response['errors'] = errors
    response['message'] = message
    response['valid'] = valid

    return response


def check_file(filename: Path) -> dict:
    errors = {}
    tables, headings = AGS4.AGS4_to_dataframe(filename)

    # Required Groups
    result = check_groups(headings)
    if result:
        errors['Required Groups'] = result

    # Required BGS Groups
    result = check_bgs_groups(headings)
    if result:
        errors['Required BGS Groups'] = result

    return errors


def check_groups(headings: list) -> list:
    """ Groups must include PROJ, LOCA or HOLE, ABBR, TYPE, UNIT """
    errors = []
    desc = ''
    required = ['PROJ', 'ABBR', 'TYPE', 'UNIT']
    for group in required:
        if group not in headings:
            desc += group + ', '
    if 'LOCA' not in headings and 'HOLE' not in headings:
        desc += '(LOCA or HOLE)' + ', '
    if desc:
        desc = 'Required groups not present: ' + desc
        desc = desc.rstrip(', ')
    if desc:
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


def check_bgs_groups(headings: list) -> list:
    """ Groups must include HOLE and GEOL for BGS """
    errors = []
    desc = ''
    required = ['HOLE', 'GEOL']
    for group in required:
        if group not in headings:
            desc += group + ', '
    if desc:
        desc = 'Required BGS groups not present: ' + desc
        desc = desc.rstrip(', ')
    if desc:
        errors.append({'line': '-', 'group': '', 'desc': desc})

    return errors


def to_plain_text(response: dict) -> str:
    """Take JSON response from convert and render as plain text."""
    return PLAIN_TEXT_TEMPLATE.render(response)


def is_valid(filename: Path) -> bool:
    """
    Validate filename and parse returned log to determine if file is valid.
    """
    return validate(filename)['valid']


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
                'errors': {},
                'valid': False}
    return response
