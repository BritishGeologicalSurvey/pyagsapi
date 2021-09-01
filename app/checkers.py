"""Functions for checking AGS files."""
import logging
from pathlib import Path
from typing import Tuple, Optional

from python_ags4 import AGS4

from app.bgs_rules import BGS_RULES

logger = logging.getLogger(__name__)


def check_ags(filename: Path, standard_AGS4_dictionary: Optional[str] = None) -> dict:
    # Get error information from file
    try:
        errors = AGS4.check_file(filename,
                                 standard_AGS4_dictionary=standard_AGS4_dictionary)
        try:
            metadata = errors.pop('Metadata')  # This also removes it from returned errors
            dictionary = [d['desc'] for d in metadata
                          if d['line'] == 'Dictionary'][0]
        except KeyError:
            # 'Metadata' is not created for some files with errors
            dictionary = ''

    except UnicodeDecodeError as err:
        line_no = len(err.object[:err.end].split(b'\n'))
        description = err.reason
        errors = {'UnicodeDecodeError': [{'line': line_no, 'group': '', 'desc': description}]}
        dictionary = ''

    return dict(errors=errors, dictionary=dictionary)


def check_bgs(filename: Path, **kwargs) -> dict:
    """
    Validate file against BGS rules.  kwargs parameter required because some
    validation functions have keyword parameters.
    """
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

    return dict(errors=errors)


def load_AGS4_as_numeric(filename: Path) -> Tuple[dict, dict]:
    """Read AGS4 file and convert to numeric data types."""
    tables, headings = AGS4.AGS4_to_dataframe(filename)

    # Convert tables to numeric data for analysis
    for group, df in tables.items():
        tables[group] = AGS4.convert_to_numeric(df)

    return tables, headings
