"""Tests for calls to AGS functions."""
from pathlib import Path
import re

import pytest

from app import ags

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', ('All checks passed!', 3)),
    ('nonsense.ags', (r'7 error\(s\) found in file!', 0)),
    ('empty.ags', (r'4 error\(s\) found in file!', 0)),
    ('real/A3040_03.ags', (r'5733 error\(s\) found in file!', 258)),
    ('example1.xlsx', ('ERROR: Only .ags files are accepted as input.', 11)),
    ('random_binary.ags', ('UnicodeDecodeError: .* in position 0', 1)),
])
def test_validate(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    expected_message, expected_size = expected

    # Act
    response = ags.validate(filename)

    # Assert
    assert f"File Name: \t {filename.name}" in response
    assert f"File Size: \t {expected_size:n} kB" in response
    assert re.search(expected_message, response)


@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', 'SUCCESS: example1.ags converted to example1.xlsx'),
    ('example1.xlsx', 'SUCCESS: example1.xlsx converted to example1.ags'),
])
def test_convert(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    converted_file, logfile = ags.convert(filename, results_dir)

    # Assert
    output = logfile.read_text()
    assert converted_file is not None and converted_file.exists()
    assert expected in output


@pytest.mark.parametrize('filename, expected', [
    ('nonsense.ags', 'IndexError: At least one sheet must be visible'),
    ('empty.ags', 'IndexError: At least one sheet must be visible'),
    ('dummy.xlsx', "AttributeError: 'DataFrame' object has no attribute 'HEADING'"),
    ('random_binary.ags', 'IndexError: At least one sheet must be visible'),
    ('real/A3040_03.ags', "UnboundLocalError: local variable 'group' referenced before assignment"),
])
def test_convert_bad_files(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    converted_file, logfile = ags.convert(filename, results_dir)

    # Assert
    output = logfile.read_text()
    assert converted_file is None
    assert 'ERROR:' in output
    assert re.search(expected, output)
