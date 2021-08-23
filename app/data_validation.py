"""Functions to validate the data within AGS files"""
from pathlib import Path
import pandas as pd
from python_ags4 import AGS4


def validate_eastings_and_northings(filename: Path) -> dict:
    """Confirm that eastings and northings lie within reasonable range."""
    # Data section of file must be extracted and converted to numeric type
    data, headings = AGS4.AGS4_to_dataframe(filename)
    loca = data['LOCA']
    loca = loca.loc[loca['HEADING'] == 'DATA', loca.columns[1:]].set_index('LOCA_ID')
    loca = loca.apply(pd.to_numeric)
    assert loca['LOCA_NATE'] > 10000
    assert loca['LOCA_NATN'] > 10000
