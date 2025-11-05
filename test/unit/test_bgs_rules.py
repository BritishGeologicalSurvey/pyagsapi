"""Test functions for individual BGS rules"""
import pytest

from app.bgs_rules import BGS_RULES
from app.checkers import load_ags4_as_numeric
from test.fixtures import BGS_RULES_ERRORS, TEST_FILE_DIR


def test_required_groups():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'required_groups.ags'
    expected = {'line': '-',
                'group': '',
                'desc': 'Required groups not present: ABBR, TYPE, UNIT, (LOCA or HOLE)'}
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Required Groups'](tables)

    assert errors == [expected]


def test_required_bgs_groups():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'required_bgs_groups.ags'
    expected = {'line': '-',
                'group': '',
                'desc': 'Required BGS groups not present: GEOL'}
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Required BGS Groups'](tables)

    assert errors == [expected]


def test_spatial_referencing():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'spatial_referencing.ags'
    expected = {'line': '-',
                'group': 'LOCA',
                'desc': 'Spatial referencing system not in LOCA_GREF, LOCA_LREF or LOCA_LLZ'}
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Spatial Referencing'](tables)

    assert errors == [expected]


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
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Drill Depth Present'](tables)

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
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Drill Depth GEOL Record'](tables)

    assert errors == expected


def test_loca_eastings_and_northings():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'loca_eastings_and_northings.ags'
    expected = [
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Null)',
         'group': 'LOCA',
         'line': 14},
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Zero)',
         'group': 'LOCA',
         'line': 15},
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Null-e)',
         'group': 'LOCA',
         'line': 16},
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Zero-e)',
         'group': 'LOCA',
         'line': 17},
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Null-n)',
         'group': 'LOCA',
         'line': 18},
        {'desc': 'LOCA_NATE / LOCA_NATN contains zeros or null values (Zero-n)',
         'group': 'LOCA',
         'line': 19},
        {'desc': 'NATE / NATN outside UK Offshore EEA or Onshore Northern Ireland '
                 'boundary (Paris)',
         'group': 'LOCA',
         'line': 13},
        {'desc': 'NATE / NATN outside Onshore Great Britain or Northern Ireland '
                 'boundaries (Derry)',
         'group': 'LOCA',
         'line': 1},
        {'desc': 'NATE / NATN outside Onshore Great Britain or Northern Ireland '
                 'boundaries (MorayFirth)',
         'group': 'LOCA',
         'line': 12},
        {'desc': 'NATE / NATN outside Onshore Great Britain or Northern Ireland '
                 'boundaries (Paris)',
         'group': 'LOCA',
         'line': 13},
        {'desc': 'NATE / NATN in Northern Ireland but LOCA_GREF undefined (Belfast)',
         'group': 'LOCA',
         'line': 3}
    ]

    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Eastings/Northings'](tables)

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
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: LOCA_LOCX is not duplicate of other column'](tables)

    assert errors == expected


def test_loca_locx_is_not_duplicate_of_other_column_lon_is_dms():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'locax_is_duplicate_lon_is_dms.ags'
    expected = [
        {'desc': 'LOCX / LOCY duplicates NATE / NATN (Duplicate NATE)',
         'group': 'LOCA',
         'line': '-'},
    ]
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: LOCA_LOCX is not duplicate of other column'](tables)

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
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: LOCA_ID references'](tables)

    assert errors == expected


def test_non_numeric_coord_types():
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / 'non_numeric_coord_types.ags'
    expected = {'BGS data validation: Non-numeric coordinate types': [
        {"desc": "Coordinate columns have non-numeric TYPE: LOCA_NATE (X), LOCA_NATN (X)",
         "group": "LOCA",
         "line": "-"}
    ]}

    _, _, errors = load_ags4_as_numeric(filename)

    assert errors == expected


@pytest.mark.parametrize('filename, expected', [
    ('sample_referencing_samp_ids.ags', BGS_RULES_ERRORS['sample_referencing_samp_ids.ags']),
    ('sample_referencing_comp_ids.ags', BGS_RULES_ERRORS['sample_referencing_comp_ids.ags']),
    ('sample_referencing_mix_ids.ags', BGS_RULES_ERRORS['sample_referencing_mix_ids.ags']),
    ('trit_group_test.ags', BGS_RULES_ERRORS['trit_group_test.ags']),
])
def test_sample_referential_integrity(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / 'bgs_rules' / filename
    tables, _, _ = load_ags4_as_numeric(filename)

    errors = BGS_RULES['BGS data validation: Sample Referencing'](tables)

    assert errors == expected
