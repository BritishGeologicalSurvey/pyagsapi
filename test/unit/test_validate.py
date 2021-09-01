"""Tests for calls to validate function."""
import datetime as dt
from pathlib import Path

from freezegun import freeze_time
import pytest

from app import ags
from app import validate
from test.fixtures import (DICTIONARIES, FROZEN_TIME, ISVALID_RSP_DATA)
from test.fixtures_json import JSON_RESPONSES
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def mock_check_ags(filename, standard_AGS4_dictionary=None):
    return dict(checker='ags', dictionary='some_dict',
                errors={})


def mock_check_bgs(filename, **kwargs):
    return dict(checker='bgs',
                errors={'BGS': [{}]})


@freeze_time(FROZEN_TIME)
def test_validate_default_checker():
    """Simulate a valid file with AGS checker"""
    # Arrange
    filename = TEST_FILE_DIR / 'does_not_matter.ags'
    expected = {
        'checkers': ['ags'],
        'dictionary': 'some_dict',
        'errors': {},
        'filename': filename.name,
        'filesize': 0,
        'message': 'All checks passed!',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'valid': True}

    # Act
    response = validate.validate(filename, checkers=[mock_check_ags])

    # Assert
    response == expected


@freeze_time(FROZEN_TIME)
def test_validate_bgs_checker():
    """Simulate a failing file with BGS checker."""
    # Arrange
    filename = TEST_FILE_DIR / 'does_not_matter.ags'
    expected = {
        'checkers': ['bgs'],
        'dictionary': '',
        'errors': {'BGS': [{}]},
        'filename': filename.name,
        'filesize': 0,
        'message': '1 error(s) found in file!',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'valid': False}

    # Act
    response = validate.validate(filename, checkers=[mock_check_bgs])

    # Assert
    response == expected


@freeze_time(FROZEN_TIME)
def test_validate_both_checkers():
    """Simulate a combination with both checkers."""
    # Arrange
    filename = TEST_FILE_DIR / 'does_not_matter.ags'
    expected = {
        'checkers': ['bgs', 'ags'],
        'dictionary': 'some_dict',
        'errors': {'BGS': [{}]},
        'filename': filename.name,
        'filesize': 0,
        'message': '1 error(s) found in file!',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'valid': False}

    # Act
    response = validate.validate(filename, checkers=[mock_check_bgs, mock_check_ags])

    # Assert
    response == expected


@freeze_time(FROZEN_TIME)
def test_validate_non_ags():
    # Arrange
    filename = TEST_FILE_DIR / 'bad.extension'
    expected = {
        'checkers': [],
        'dictionary': '',
        'errors': {'Non .ags extension': [
            {'desc': 'bad.extension is not an .ags file', 'group': '', 'line': '-'}]},
        'filename': 'bad.extension',
        'filesize': 0,
        'message': '1 error(s) found in file!',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'valid': False}

    # Act
    response = validate.validate(filename)

    # Assert
    response == expected


@freeze_time(FROZEN_TIME)
@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
def test_validate(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    response = validate.validate(filename)

    # Assert
    # Check that metadata fields are correct
    for key in ['filename', 'filesize', 'checkers', 'time', 'dictionary',
                'errors', 'message', 'valid']:
        assert response[key] == expected[key]


@pytest.mark.parametrize('dictionary', DICTIONARIES.values())
def test_validate_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    response = validate.validate(filename,
                                 standard_AGS4_dictionary=dictionary)

    # Assert
    assert response['filename'] == 'example_ags.ags'
    assert response['dictionary'] == dictionary


def test_validate_custom_dictionary_bad_file():
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'
    dictionary = 'bad_file.ags'

    # Act
    with pytest.raises(ValueError) as err:
        validate.validate(filename, standard_AGS4_dictionary=dictionary)

    # Assert
    message = str(err.value)
    assert 'dictionary' in message
    for key in ags.STANDARD_DICTIONARIES:
        assert key in message


@pytest.mark.parametrize('filename, expected', ISVALID_RSP_DATA)
def test_is_valid(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = validate.is_valid(filename)

    # Assert
    assert result == expected


@pytest.mark.parametrize('dictionary', DICTIONARIES.values())
def test_is_valid_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    result = validate.is_valid(filename,
                               standard_AGS4_dictionary=dictionary)

    # Assert
    assert result


@pytest.mark.parametrize('filename', [
    'example_ags.ags', 'nonsense.ags', 'random_binary.ags',
    'real/Blackburn Southern Bypass.ags'])
def test_to_plain_text(filename):
    # Arrange
    response = JSON_RESPONSES[filename]
    expected = PLAIN_TEXT_RESPONSES[filename]

    # Act
    text = validate.to_plain_text(response)

    # Assert
    assert text.strip() == expected.strip()
