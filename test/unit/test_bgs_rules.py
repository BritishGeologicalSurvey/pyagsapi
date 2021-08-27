"""Test functions for individual BGS rules"""
from pathlib import Path

from app.bgs_rules import BGS_RULES
from app.bgs import load_AGS4_as_numeric

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_required_groups():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'required_groups.ags'
    expected = {'line': '-',
                'group': '',
                'desc': 'Required groups not present: ABBR, TYPE, UNIT, (LOCA or HOLE)'}
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Required Groups'](tables)

    assert errors == [expected]


def test_required_bgs_groups():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'required_bgs_groups.ags'
    expected = {'line': '-',
                'group': '',
                'desc': 'Required BGS groups not present: GEOL'}
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Required BGS Groups'](tables)

    assert errors == [expected]


def test_spatial_referencing():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'spatial_referencing.ags'
    expected = {'line': '-',
                'group': 'LOCA',
                'desc': 'Spatial referencing system not in LOCA_GREF, LOCA_LREF or LOCA_LLZ!'}
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Spatial Referencing'](tables)

    assert errors == [expected]
