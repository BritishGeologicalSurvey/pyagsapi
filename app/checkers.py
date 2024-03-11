"""
checker functions check a file against the rules.  They also catch errors
to do with opening the files.
"""
import logging
from pathlib import Path
import re
from typing import Tuple, Optional, Dict, List

import python_ags4
from python_ags4 import AGS4
import pandas as pd

from app.bgs_rules import BGS_RULES, bgs_rules_version

logger = logging.getLogger(__name__)


def check_ags(filename: Path, standard_AGS4_dictionary: Optional[str] = None) -> dict:
    if standard_AGS4_dictionary:
        dictionary_file = Path(standard_AGS4_dictionary).name
    else:
        dictionary_file = 'None supplied'
    logger.info("Checking %s against AGS rules (Dictionary: %s).",
                filename.name, dictionary_file)

    # Get error information from file
    try:
        errors = AGS4.check_file(filename,
                                 standard_AGS4_dictionary=standard_AGS4_dictionary)
        try:
            metadata = errors.pop('Metadata')  # This also removes it from returned errors
            dictionary = [d['desc'] for d in metadata
                          if d['line'] == 'Dictionary'][0]
        except (KeyError, IndexError):
            # 'Metadata' is not created for some files with errors
            # or 'Dictionary' is not set in Metadata'
            dictionary = ''

    except UnicodeDecodeError as err:
        line_no = len(err.object[:err.end].split(b'\n'))
        description = f"UnicodeDecodeError: {err.reason}"
        errors = {'File read error': [{'line': line_no, 'group': '', 'desc': description}]}
        dictionary = ''

    # Use summary from errors dictionary is available
    summary = errors.pop('Summary of data', [])

    return dict(checker=f'python_ags4 v{python_ags4.__version__}',
                errors=errors, dictionary=dictionary, summary=summary)


def check_bgs(filename: Path, **kwargs) -> dict:
    """
    Validate file against BGS rules.  kwargs parameter required because some
    validation functions have keyword parameters.
    """
    logger.info("Checking %s against BGS rules.", filename.name)
    errors = {}
    load_error = None
    bgs_metadata = {}

    tables, load_error, ags4_errors = load_tables_reporting_errors(filename)

    if load_error:
        errors['File read error'] = [{'line': '-', 'group': '', 'desc': load_error}]
    else:
        errors.update(ags4_errors)
        # Get additional metadata
        bgs_metadata = generate_bgs_metadata(tables)

        # Apply checks
        for rule, func in BGS_RULES.items():
            logger.info("Checking against %s", rule)
            result = func(tables)
            if result:
                errors[rule] = result

    return dict(checker=f'bgs_rules v{bgs_rules_version}',
                errors=errors,
                additional_metadata=bgs_metadata)


def load_tables_reporting_errors(filename):
    tables = None
    ags4_errors = {}

    try:
        # Try to load and convert the file.  Coordinate type errors replace
        # empty dictionary from outer scope
        tables, _, ags4_errors = load_ags4_as_numeric(filename)
        load_error = None
    except UnboundLocalError:
        # This error is thrown in response to a bug in the upstream code,
        # which in turn is only triggered if the AGS file has duplicate
        # headers.
        load_error = "ERROR: File contains duplicate headers"
    except AGS4.AGS4Error as err:
        load_error = str(err)
    except IndexError:
        load_error = "ERROR: File cannot be read, please use AGS checker to confirm format errors"

    return tables, load_error, ags4_errors


def generate_bgs_metadata(tables: Dict[str, pd.DataFrame]) -> dict:
    """Generate additional metadata from groups."""
    try:
        projects = tables['PROJ'].apply(lambda row: f"{row['PROJ_ID']} ({row['PROJ_NAME']})", axis=1).to_list()
    except KeyError:
        projects = []

    try:
        loca_rows = len(tables['LOCA'][tables['LOCA']['HEADING'] == 'DATA'])
    except KeyError:
        loca_rows = 0

    groups = tables.keys()
    bgs_metadata = {
        'bgs_all_groups': f'{len(groups)} groups identified in file: {" ".join(groups)}',
        'bgs_file': f'Optional FILE group present: {"FILE" in groups}',
        'bgs_dict': f'Optional DICT group present: {"DICT" in groups}',
        'bgs_loca_rows': f'{loca_rows} data row(s) in LOCA group',
        'bgs_projects': f'{len(projects)} projects found: {"; ".join(projects)}',
    }
    return bgs_metadata


def load_ags4_as_numeric(filename: Path) -> Tuple[dict, dict, List[dict]]:
    """Read AGS4 file and convert to numeric data types."""
    tables, headings = AGS4.AGS4_to_dataframe(filename)

    # Check the TYPE of coordinate in LOCA
    coord_columns = ['LOCA_NATE', 'LOCA_NATN', 'LOCA_LOCX', 'LOCA_LOCY']
    errors = get_coord_column_type_errors(tables, coord_columns)

    # Convert tables to numeric data for analysis
    for group, df in tables.items():
        tables[group] = AGS4.convert_to_numeric(df)

    # Force conversion of LOCA coordinate columns, even if type is not numeric
    if tables:
        for column in coord_columns:
            try:
                tables['LOCA'][column] = pd.to_numeric(tables['LOCA'][column])
            except KeyError:
                # Not all files have all columns
                pass

    return tables, headings, errors


def get_coord_column_type_errors(tables: dict, coord_columns: List[str]) -> dict:
    """
    Check the coordinate columns in LOCA table have correct data type and
    return errors for those that don't.
    """
    try:
        loca = tables['LOCA']
    except KeyError:
        # If LOCA doesn't exist, other errors are returned elsewhere
        return {}

    bad_columns = []
    for column in coord_columns:
        try:
            type_ = loca.loc[loca['HEADING'] == 'TYPE', column].tolist()[0]
            if not re.search(r'(DP|MC|SF|SCI)', type_):
                bad_columns.append(f"{column} ({type_})")
        except KeyError:
            # Ignore columns that don't exist
            pass

    if bad_columns:
        error_message = f"Coordinate columns have non-numeric TYPE: {', '.join(bad_columns)}"
        errors = {"BGS data validation: Non-numeric coordinate types":
                  [{'line': '-', 'group': 'LOCA', 'desc': error_message}]}
    else:
        errors = {}

    return errors
