"""Functions to handle the BGS parser."""
import datetime as dt
from functools import reduce
import logging
from pathlib import Path
from typing import Optional, Tuple

from python_ags4 import AGS4

from app import ags
from app.bgs_rules import BGS_RULES
from app.response_templates import PLAIN_TEXT_TEMPLATE


logger = logging.getLogger(__name__)


def validate(filename: Path,
             ags_validation: Optional[bool] = False,
             standard_AGS4_dictionary: Optional[str] = None) -> dict:
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
        if ags_validation:
            response = ags.validate(filename, standard_AGS4_dictionary=standard_AGS4_dictionary)
        bgs_errors = check_file(filename)
        if response['errors']:
            errors = dict(response['errors'], **bgs_errors)
        else:
            errors = bgs_errors
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
        message = 'Unable to open file.'
        valid = False

    # Add error info to response
    response['errors'] = errors
    response['message'] = message
    response['valid'] = valid

    return response


def check_file(filename: Path) -> dict:
    errors = {}
    error_message = None

    try:
        # Try to load and convert the file
        tables, headers = load_AGS4_as_numeric(filename)
    except IndexError:
        # This error is triggered by AGS3 files
        error_message = "ERROR: File does not have AGS4 format layout"
    except UnboundLocalError:
        # This error is thrown in response to a bug in the upstream code,
        # which in turn is only triggered if the AGS file has duplicate
        # headers.
        error_message = "ERROR: File contains duplicate headers"
    except SystemExit:
        #  There are two function calls in python_ags4.AGS4 that throw a
        # sys.exit in reponse to a bad file.  The associated errors are
        # summarised here.
        error_message = "ERROR: UNIT and/or TYPE rows missing OR mismatched column numbers"

    if error_message:
        errors['File read error'] = [{'line': '-', 'group': '', 'desc': error_message}]
    else:
        for rule, func in BGS_RULES.items():
            result = func(tables)
            if result:
                errors[rule] = result

    return errors


def load_AGS4_as_numeric(filename: Path) -> Tuple[dict, dict]:
    """Read AGS4 file and convert to numeric data types."""
    tables, headings = AGS4.AGS4_to_dataframe(filename)

    # Convert tables to numeric data for analysis
    for group, df in tables.items():
        tables[group] = AGS4.convert_to_numeric(df)

    return tables, headings


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
