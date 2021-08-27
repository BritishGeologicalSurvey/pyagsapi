"""Tests for calls to BGS functions."""
from pathlib import Path

import pytest

from app import bgs

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'

BGS_FILE_DATA = {
    'example_ags.ags': ('2 error(s) found in file!', False),
    'empty.ags': ('2 error(s) found in file!', False),
    'real/43370.ags': ('All checks passed!', True),
    'extension_is.bad': ('ERROR: extension_is.bad is not .ags format', False),
    'real/JohnStPrimarySchool.ags': ('1 error(s) found in file!', False),
    'real/19684.ags': ('2 error(s) found in file!', False),
}

AGS_FILE_DATA = {
    'example_ags.ags': ('2 error(s) found in file!', False),
    'empty.ags': ('6 error(s) found in file!', False),
    'real/43370.ags': ('139 error(s) found in file!', False),
    'extension_is.bad': ('ERROR: extension_is.bad is not .ags format', False),
}


@pytest.mark.parametrize('filename, expected',
                         [item for item in BGS_FILE_DATA.items()])
def test_validate(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    expected_message, expected_valid = expected

    # Act
    response = bgs.validate(filename)

    # Assert
    # Check that metadata fields are correct
    keys = {'filename', 'filesize', 'time', 'errors', 'message', 'valid'}
    assert set(response.keys()) == keys
    assert response['message'] == expected_message
    assert response['valid'] == expected_valid


@pytest.mark.parametrize('filename, expected',
                         [item for item in AGS_FILE_DATA.items()])
def test_validate_ags(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    expected_message, expected_valid = expected

    # Act
    response = bgs.validate(filename, ags_validation=True)

    # Assert
    # Check that metadata fields are correct
    keys = {'filename', 'filesize', 'time', 'checker', 'dictionary', 'errors', 'message', 'valid'}
    assert set(response.keys()).issubset(keys)
    assert response['message'] == expected_message
    assert response['valid'] == expected_valid


@pytest.mark.parametrize('filename, expected',
                         [item for item in BGS_FILE_DATA.items()])
def test_is_valid(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    expected_valid = expected[1]

    # Act
    result = bgs.is_valid(filename)

    # Assert
    assert result == expected_valid


@pytest.mark.parametrize('filename', BGS_FILE_DATA.keys())
def test_to_plain_text(filename):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    response = bgs.validate(filename)
    text = bgs.to_plain_text(response)

    # Assert
    assert text
