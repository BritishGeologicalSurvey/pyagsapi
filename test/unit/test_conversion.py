"""Tests for calls to AGS functions."""
from pathlib import Path
import re

import pytest

from app.conversion import convert
from test.fixtures import (BAD_FILE_DATA, GOOD_FILE_DATA)

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


@pytest.mark.parametrize('filename, expected', GOOD_FILE_DATA)
def test_convert(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()
    expected_message, expected_new_file_name = expected

    # Act
    converted_file, response = convert(filename, results_dir)

    # Assert
    assert converted_file is not None and converted_file.exists()
    assert response['filename'] == filename.name
    assert re.search(expected_message, response['message'])


@pytest.mark.parametrize('filename, expected', BAD_FILE_DATA)
def test_convert_bad_files(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()
    expected_message, expected_size = expected

    # Act
    converted_file, response = convert(filename, results_dir)

    # Assert
    assert converted_file is None
    assert response['filename'] == filename.name
    assert response['filesize'] == expected_size
    assert response['message'] == expected_message
