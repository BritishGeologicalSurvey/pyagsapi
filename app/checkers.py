"""
checker functions check a file against the rules.  They also catch errors
to do with opening the files.
"""
import logging
from pathlib import Path
from typing import Tuple, Optional

import python_ags4
from python_ags4 import AGS4
import pandas as pd

from app.bgs_rules import BGS_RULES, bgs_rules_version

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
        description = f"UnicodeDecodeError: {err.reason}"
        errors = {'File read error': [{'line': line_no, 'group': '', 'desc': description}]}
        dictionary = ''

    return dict(checker=f'python_ags4 v{python_ags4.__version__}',
                errors=errors, dictionary=dictionary)


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

    return dict(checker=f'bgs_rules v{bgs_rules_version}',
                errors=errors)


def load_AGS4_as_numeric(filename: Path) -> Tuple[dict, dict]:
    """Read AGS4 file and convert to numeric data types."""
    tables, headings = AGS4.AGS4_to_dataframe(filename)

    # Convert tables to numeric data for analysis
    for group, df in tables.items():
        tables[group] = AGS4.convert_to_numeric(df)

    # Force conversion of coordinate columns, even if type says text
    coord_columns = ['LOCA_NATE', 'LOCA_NATN', 'LOCA_LOCX', 'LOCA_LOCY']
    if tables:
        for column in coord_columns:
            try:
                tables['LOCA'][column] = pd.to_numeric(tables['LOCA'][column])
            except KeyError:
                # Not all files have all columns
                pass

    return tables, headings
