"""Tests for calls to AGS functions."""
from pathlib import Path
import re

from freezegun import freeze_time
import pytest

from app import ags
from test.fixtures import BAD_FILE_DATA, FROZEN_TIME, GOOD_FILE_DATA, ISVALID_RSP_DATA
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
    response = ags.validate(filename)

    # Assert
    # Check that metadata fields are correct
    for key in ['filename', 'filesize', 'checker', 'time', 'dictionary',
                'errors', 'message', 'valid']:
        assert response[key] == expected[key]


@pytest.mark.parametrize('dictionary', [
     "Standard_dictionary_v4_0_3.ags",
     "Standard_dictionary_v4_0_4.ags",
     "Standard_dictionary_v4_1.ags"])
def test_validate_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example1.ags'

    # Act
    response = ags.validate(filename,
                            standard_AGS4_dictionary=dictionary)

    # Assert
    assert response['filename'] == 'example1.ags'
    assert response['dictionary'] == dictionary


def test_validate_custom_dictionary_bad_file():
    # Arrange
    filename = TEST_FILE_DIR / 'example1.ags'
    dictionary = 'bad_file.ags'

    # Act
    with pytest.raises(ValueError) as err:
        ags.validate(filename, standard_AGS4_dictionary=dictionary)

    # Assert
    message = str(err.value)
    assert 'dictionary' in message
    for key in ags.STANDARD_DICTIONARIES:
        assert key in message


@pytest.mark.parametrize('filename, expected', GOOD_FILE_DATA)
def test_convert(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    converted_file, log = ags.convert(filename, results_dir)

    # Assert
    assert converted_file is not None and converted_file.exists()
    assert re.search(expected, log)


@pytest.mark.parametrize('filename, expected', BAD_FILE_DATA)
def test_convert_bad_files(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()
    expected_message, expected_size = expected

    # Act
    converted_file, log = ags.convert(filename, results_dir)

    # Assert
    assert converted_file is None
    assert f"File Name: \t {filename.name}" in log
    assert f"File Size: \t {expected_size:n} kB" in log
    assert 'ERROR:' in log
    assert re.search(expected_message, log)


@pytest.mark.parametrize('filename, expected', ISVALID_RSP_DATA)
def test_is_valid(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = ags.is_valid(filename)

    # Assert
    assert result == expected


@pytest.mark.parametrize('dictionary', [
     "Standard_dictionary_v4_0_3.ags",
     "Standard_dictionary_v4_0_4.ags",
     "Standard_dictionary_v4_1.ags"])
def test_is_valid_custom_dictionary(dictionary):
    # Arrange
    filename = TEST_FILE_DIR / 'example1.ags'

    # Act
    result = ags.is_valid(filename,
                          standard_AGS4_dictionary=dictionary)

    # Assert
    assert result


@pytest.mark.parametrize('filename', [
    'example1.ags', 'nonsense.ags', 'random_binary.ags',
    'real/Blackburn Southern Bypass.ags'])
def test_to_plain_text(filename):
    # Arrange
    response = JSON_RESPONSES[filename]
    expected = PLAIN_TEXT_RESPONSES[filename]

    # Act
    text = ags.to_plain_text(response)

    # Assert
    assert text.strip() == expected.strip()
