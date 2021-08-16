"""Tests for calls to AGS functions."""
from pathlib import Path

import pytest

from app import ags

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_validate(tmp_path):
    # Arrange
    filename = TEST_FILE_DIR / 'example1.ags'
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    ags.validate(filename, results_dir)

    # Assert
    results_file = results_dir / 'example1.log'
    output = results_file.read_text()
    assert 'example1.ags' in output
    assert 'All checks passed!' in output


def test_validate_non_ags_suffix(tmp_path):
    # Arrange
    filename = TEST_FILE_DIR / 'example1.xlsx'
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    with pytest.raises(ags.Ags4CliError):
        ags.validate(filename, results_dir)


def test_validate_binary_file(tmp_path):
    # Arrange
    filename = TEST_FILE_DIR / 'random_binary.ags'
    results_dir = tmp_path / 'results'
    if not results_dir.exists:
        results_dir.mkdir()

    # Act
    with pytest.raises(ags.Ags4CliError):
        ags.validate(filename, results_dir)
