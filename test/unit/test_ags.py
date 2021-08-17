"""Tests for calls to AGS functions."""
from pathlib import Path
import re

import pytest

from app import ags

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', 'All checks passed!'),
    ('nonsense.ags', r'7 error\(s\) found in file!'),
    ('empty.ags', r'4 error\(s\) found in file!'),
])
def test_validate(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    logfile = ags.validate(filename, results_dir)

    # Assert
    output = logfile.read_text()
    assert f"File Name: \t {filename.name}" in output
    assert re.search(expected, output)


@pytest.mark.parametrize('filename, expected', [
    ('example1.xlsx', 'ERROR: Only .ags files are accepted as input.'),
    ('random_binary.ags', 'UnicodeDecodeError: .* in position 0'),
])
def test_validate_unreadable_files(tmp_path, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    logfile = ags.validate(filename, results_dir)

    # Assert
    output = logfile.read_text()
    assert f"File Name: \t {filename.name}" in output
    assert re.search(expected, output)
