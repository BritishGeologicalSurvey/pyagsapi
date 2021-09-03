"""Test functions for individual BGS rules"""
from pathlib import Path

from app.bgs_rules import BGS_RULES
from app.checkers import load_AGS4_as_numeric

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


def test_eastings_northings_present():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'eastings_northings_present.ags'
    expected = [
        {'line': '-',
         'group': 'LOCA',
         'desc': 'LOCA_NATE contains zeros or null values'},
        {'line': '-',
         'group': 'LOCA',
         'desc': 'LOCA_NATN contains zeros or null values'}
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Eastings/Northings Present'](tables)

    assert errors == expected


def test_eastings_northings_range():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'eastings_northings_range.ags'
    expected = [
        {'line': '-',
         'group': 'LOCA',
         'desc': 'LOCA_NATE values outside 100,000 to 800,000 range'},
        {'line': '-',
         'group': 'LOCA',
         'desc': 'LOCA_NATN values outside 100,000 to 1,400,000 range'},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Eastings/Northings Range'](tables)

    assert errors == expected


def test_drill_depth_present():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'drill_depth_present.ags'
    expected = [
        {'line': '-',
         'group': 'HDPH',
         'desc': 'HDPH_TOP contains null values'},
        {'line': '-',
         'group': 'HDPH',
         'desc': 'HDPH_BASE contains zero or null values'},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Drill Depth Present'](tables)

    assert errors == expected


def test_drill_depth_geol_record():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'drill_depth_geol_record.ags'
    expected = [
        {'line': '-', 'group': 'HDPH',
         'desc': "HDPH LOCA_IDs not in GEOL group ({'BH108'})"},
        {'line': '-', 'group': 'HDPH',
         'desc': "GEOL LOCA_IDs not in HDPH group ({'BH109'})"},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Drill Depth GEOL Record'](tables)

    assert errors == expected
