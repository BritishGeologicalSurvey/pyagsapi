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
    ('random_binary.ags', ('ERROR: Unreadable character "á" at position 1 on line: 1\nStarting:', 1)),
    ('real/CG014058_F.ags', (r'ERROR: Unreadable character "æ" at position 80 on line: 263\nStarting: "WS2"', 49)),
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
    converted_file, log = ags.convert(filename, results_dir)

    # Assert
    assert converted_file is not None and converted_file.exists()
    assert re.search(expected, log)


@pytest.mark.parametrize('filename, expected', [
    ('nonsense.ags', ('IndexError: At least one sheet must be visible', 0)),
    ('empty.ags', ('IndexError: At least one sheet must be visible', 0)),
    ('dummy.xlsx', ("AttributeError: 'DataFrame' object has no attribute 'HEADING'", 5)),
    ('random_binary.ags', ('IndexError: At least one sheet must be visible', 1)),
    ('real/A3040_03.ags', ("UnboundLocalError: local variable 'group' referenced before assignment", 258)),
])
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


@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', True),
    ('nonsense.ags', False),
    ('empty.ags', False),
    ('dummy.xlsx', False),
    ('random_binary.ags', False),
    ('real/A3040_03.ags', False),
])
def test_is_valid(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    result = ags.is_valid(filename)

    # Assert
    assert result == expected
