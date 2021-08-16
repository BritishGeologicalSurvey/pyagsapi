"""Tests for calls to AGS functions."""
from pathlib import Path

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
