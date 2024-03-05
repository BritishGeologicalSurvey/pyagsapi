"""These tests confirm that the checkers can handle various exceptions"""
from pathlib import Path

import pytest
import python_ags4

from app.checkers import check_bgs, check_ags
from app.bgs_rules import bgs_rules_version

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'

AGS_FILE_DATA = {
    'example_ags.ags': ('2 error(s) found in file!', False),
    'empty.ags': ('6 error(s) found in file!', False),
    'real/43370.ags': ('139 error(s) found in file!', False),
    'extension_is.bad': ('ERROR: extension_is.bad is not .ags format', False),
}


@pytest.mark.parametrize('filename, expected_rules', [
    ('example_ags.ags', set()),
    ('random_binary.ags', {'General', 'AGS Format Rule 1', 'AGS Format Rule 2a', 'AGS Format Rule 3',
                           'AGS Format Rule 5', 'AGS Format Rule 13', 'AGS Format Rule 14', 'AGS Format Rule 15',
                           'AGS Format Rule 17'}),
    ('nonsense.AGS', {'AGS Format Rule 2a', 'AGS Format Rule 3', 'AGS Format Rule 5', 'AGS Format Rule 13',
                      'AGS Format Rule 14', 'AGS Format Rule 15', 'AGS Format Rule 17'}),
    ('empty.ags', {'AGS Format Rule 13', 'AGS Format Rule 14', 'AGS Format Rule 15', 'AGS Format Rule 17'}),
    ('real/A3040_03.ags', {'AGS Format Rule 3'}),
    ('real/43370.ags', {'General', 'AGS Format Rule 2a', 'AGS Format Rule 1'}),
    ('real/JohnStPrimarySchool.ags', {'AGS Format Rule 3', 'AGS Format Rule 5', 'AGS Format Rule ?',
                                      'AGS Format Rule 4', 'AGS Format Rule 2a'}),
    ('real/19684.ags', {'AGS Format Rule 3'}),
    ('real/E52A4379 (2).ags', {'AGS Format Rule 3'}),
])
def test_check_ags(filename, expected_rules):
    """Check that broken rules are returned and exceptions handled correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_ags(filename)

    # Assert
    # Check that metadata fields are correct
    assert result['checker'] == f'python_ags4 v{python_ags4.__version__}'
    assert set(result['errors'].keys()) == expected_rules


@pytest.mark.parametrize('filename, expected_rules, file_read_message', [
    ('example_ags.ags',
     ['BGS data validation: Required BGS Groups', 'BGS data validation: Spatial Referencing'], None),
    ('random_binary.ags',
     ['BGS data validation: Required Groups', 'BGS data validation: Required BGS Groups'], None),
    ('nonsense.AGS',
     ['BGS data validation: Required Groups', 'BGS data validation: Required BGS Groups'], None),
    ('empty.ags',
     ['BGS data validation: Required Groups', 'BGS data validation: Required BGS Groups'], None),
    ('ags3.ags',
     ['File read error'], 'ERROR: File cannot be read, please use AGS checker to confirm format errors'),
    ('real/Southwark.ags',
     ['BGS data validation: Sample Referencing'], None),
    ('real/Mount Severn- Environment Agency.ags',
     ['BGS data validation: Non-numeric coordinate types', 'BGS data validation: Spatial Referencing'], None),
    ('real/A112794-16 Glenally_Road_Factual_FINAL.ags',
     ['BGS data validation: Spatial Referencing', 'BGS data validation: LOCA within Great Britain'], None),
    ('real/A3040_03.ags',
     ['File read error'], 'ERROR: File contains duplicate headers'),
    ('real/43370.ags',  # File has no errors
     [], None),
    ('real/JohnStPrimarySchool.ags',
     ['File read error'], 'Line 27 does not have the same number of entries as the HEADING row in GEOL.'),
    ('real/19684.ags',
     ['BGS data validation: Required Groups', 'BGS data validation: Required BGS Groups'], None),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', {}),
])
def test_check_bgs(filename, expected_rules, file_read_message):
    """Check different rules and file_read_messages are reported correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_bgs(filename)

    # Assert
    # Check that metadata fields are correct
    assert result['checker'] == f'bgs_rules v{bgs_rules_version}'
    assert list(result['errors'].keys()) == expected_rules
    file_read_errors = result['errors'].get('File read error')
    if file_read_errors:
        assert len(file_read_errors) == 1
        assert file_read_errors[0]['desc'] == file_read_message


@pytest.mark.parametrize('filename, expected_metadata', [
    ('empty.ags', {
        'bgs_all_groups': '0 groups identified in file: ',
        'bgs_dict': 'Optional DICT group present: False',
        'bgs_file': 'Optional FILE group present: False',
        'bgs_loca_rows': '0 data rows in LOCA group',
        'bgs_projects': '0 projects found: '
    }),
    ('example_ags.ags', {
        'bgs_all_groups': '7 groups identified in file: '
                          'PROJ ABBR TRAN TYPE UNIT LOCA SAMP',
        'bgs_dict': 'Optional DICT group present: False',
        'bgs_file': 'Optional FILE group present: False',
        'bgs_loca_rows': '1 data rows in LOCA group',
        'bgs_projects': '1 projects found: 121415 (ACME Gas Works Redevelopment)'
    }),
    ('real/Southwark.ags', {
        'bgs_all_groups': '12 groups identified in file: '
                          'PROJ ABBR DICT TRAN TYPE UNIT CHIS GEOL ISPT LOCA SAMP WSTG',
        'bgs_dict': 'Optional DICT group present: True',
        'bgs_file': 'Optional FILE group present: False',
        'bgs_loca_rows': '2 data rows in LOCA group',
        'bgs_projects': '1 projects found: 7500/75 (Southwark)'}),
])
def test_check_bgs_additional_metadata(filename, expected_metadata):
    """Check addtional metadata is added correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_bgs(filename)

    # Assert
    assert result['additional_metadata'] == expected_metadata
