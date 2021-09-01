"""These tests confirm that the checkers can handle various exceptions"""
from pathlib import Path

import pytest

from app.checkers import check_bgs
from app.bgs_rules import bgs_rules_version

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'

AGS_FILE_DATA = {
    'example_ags.ags': ('2 error(s) found in file!', False),
    'empty.ags': ('6 error(s) found in file!', False),
    'real/43370.ags': ('139 error(s) found in file!', False),
    'extension_is.bad': ('ERROR: extension_is.bad is not .ags format', False),
}


@pytest.mark.parametrize('filename, expected', [
    ('example_ags.ags', None),
    ('nonsense.ags', None),
    ('empty.ags', None),
    ('real/A3040_03.ags', 'ERROR: File contains duplicate headers'),
    ('real/43370.ags', 'ERROR: UNIT and/or TYPE rows missing OR mismatched column numbers'),
    ('real/JohnStPrimarySchool.ags', 'ERROR: UNIT and/or TYPE rows missing OR mismatched column numbers'),
    ('real/19684.ags', None),
    # This file crashes because it asks for user input
    # ('real/E52A4379 (2).ags', {}),
])
def test_check_bgs(filename, expected):
    """Check that File read errors are handled and reported correctly."""
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = check_bgs(filename)

    # Assert
    # Check that metadata fields are correct
    assert result['checker'] == f'bgs_rules v{bgs_rules_version}'
    errors = result['errors'].get('File read error')
    if errors:
        assert len(errors) == 1
        assert errors[0]['desc'] == expected
