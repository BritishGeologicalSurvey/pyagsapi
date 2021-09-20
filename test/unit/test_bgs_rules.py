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


def test_loca_within_great_britain():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'loca_within_great_britain.ags'
    expected = [
        {'desc': 'NATE / NATN outside Great Britain and Northern Ireland (Bad NATE)',
         'group': 'LOCA',
         'line': '-'},
        {'desc': 'NATE / NATN outside Great Britain and Northern Ireland (Bad NATN)',
         'group': 'LOCA',
         'line': '-'},
        {'desc': 'NATE / NATN outside Great Britain and Northern Ireland (Derry)',  # these coords given in EPSG:27700
         'group': 'LOCA',
         'line': '-'},
        {'desc': 'NATE / NATN in Northern Ireland but LOCA_GREF undefined (Belfast)',
         'group': 'LOCA',
         'line': '-'}
    ]

    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['LOCA within Great Britain'](tables)

    assert errors == expected


def test_loca_locx_is_not_duplicate_of_other_column():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'locax_is_duplicate.ags'
    expected = [
        {'desc': 'LOCX / LOCY duplicates NATE / NATN (Duplicate NATE)',
         'group': 'LOCA',
         'line': '-'},
        {'desc': 'LOCX / LOCY duplicates LON / LAT (Duplicate LAT)',
         'group': 'LOCA',
         'line': '-'},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['LOCA_LOCX is not duplicate of other column'](tables)


def test_sample_referential_integrity_no_key():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'sample_referencing_no_key.ags'
    expected = [
        {'line': '-', 'group': 'SAMP',
         'desc': "No sample id: either SAMP_ID or (LOCA_ID,SAMP_TOP,SAMP_TYPE,SAMP_REF)"},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['Sample Referencing'](tables)

    assert errors == expected


def test_loca_references_are_valid():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'loca_references_are_valid.ags'
    expected = [
        {'desc': 'Record 2 has missing LOCA_ID',
         'group': 'HDPH',
         'line': '-'},
        {'desc': 'LOCA_ID (Sydney) is not found in LOCA group',
         'group': 'SAMP',
         'line': '-'},
    ]
    tables, _ = load_AGS4_as_numeric(filename)

    errors = BGS_RULES['LOCA_ID references'](tables)

    assert errors == expected
