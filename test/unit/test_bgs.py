"""Tests for calls to AGS functions."""
from pathlib import Path

from app import bgs

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_validate():
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    response = bgs.validate(filename)

    # Assert
    # Check that metadata fields are correct
    keys = {'filename', 'filesize', 'time', 'errors', 'message', 'valid'}
    assert set(response.keys()) == keys


def test_is_valid():
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    result = bgs.is_valid(filename)

    # Assert
    assert result


def test_to_plain_text():
    # Arrange
    filename = TEST_FILE_DIR / 'example_ags.ags'

    # Act
    response = bgs.validate(filename)
    text = bgs.to_plain_text(response)

    # Assert
    assert text
