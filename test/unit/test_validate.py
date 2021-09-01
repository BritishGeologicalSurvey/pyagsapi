"""Tests for calls to validate function."""
from pathlib import Path

from freezegun import freeze_time
import pytest

from app import ags
from app.validate import validate
from test.fixtures import (DICTIONARIES, FROZEN_TIME, ISVALID_RSP_DATA)
from test.fixtures_json import JSON_RESPONSES
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


@freeze_time(FROZEN_TIME)
@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
def test_validate(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    response = validate(filename)

    # Assert
    # Check that metadata fields are correct
    for key in ['filename', 'filesize', 'checker', 'time', 'dictionary',
                'errors', 'message', 'valid']:
        assert response[key] == expected[key]


@pytest.mark.parametrize('dictionary', DICTIONARIES.values())
def test_validate_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    response = validate(filename,
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
        validate(filename, standard_AGS4_dictionary=dictionary)

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
    result = ags.is_valid(filename)

    # Assert
    assert result == expected


@pytest.mark.parametrize('dictionary', DICTIONARIES.values())
def test_is_valid_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    result = ags.is_valid(filename,
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
    text = ags.to_plain_text(response)

    # Assert
    assert text.strip() == expected.strip()
