"""Tests for calls to AGS functions."""
import datetime as dt
from pathlib import Path
import re

from freezegun import freeze_time
import pytest

from app import ags

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'

JSON_RESPONSES = {
    'example1.ags': {
        'filename': 'example1.ags',
        'filesize': 4039,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': 'Standard_dictionary_v4_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'All checks passed!',
        'errors': []
    },
    'nonsense.ags': {
        'filename': 'nonsense.ags',
        'filesize': 9,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': 'Standard_dictionary_v4_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': [
            {'rule': 'Rule 2a',
             'errors': [
                 {'line_no': 1, 'group': '', 'desc': 'Is not terminated by <CR> and <LF> characters.'}
             ]
             },
            {'rule': 'Rule 3',
             'errors': [
                 {'line_no': 1, 'group': '', 'desc': 'Does not start with a valid data descriptor.'}
             ]
             },
            {'rule': 'Rule 5',
             'errors': [
                 {'line_no': 1, 'group': '', 'desc': 'Contains fields that are not enclosed in double quotes.'}
             ]
             },
            {'rule': 'Rule 13',
             'errors': [
                 {'line_no': 1, 'group': 'PROJ', 'desc': 'PROJ table not found.'}
             ]
             },
            {'rule': 'Rule 14',
             'errors': [
                 {'line_no': 1, 'group': 'TRAN', 'desc': 'TRAN table not found.'}
             ]
             },
            {'rule': 'Rule 15',
             'errors': [
                 {'line_no': 1, 'group': 'UNIT', 'desc': 'UNIT table not found.'}
             ]
             },
            {'rule': 'Rule 17',
             'errors': [
                 {'line_no': 1, 'group': 'TYPE', 'desc': 'TYPE table not found.'}
             ]
             },
        ]
    },
    'random_binary.ags': {
        'filename': 'random_binary.ags',
        'filesize': 1024,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': '',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': 'File could not be opened for checking.',
        'errors': [
            {'rule': 'File read error',
             'errors': [
                 {'line_no': 1, 'group': '', 'desc': 'ERROR: Unreadable character "á" at position 1'}
             ]
             },
        ]
    }
}


@freeze_time("2021-08-23 14:25:43")
@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
def test_validate(filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    response = ags.validate(filename)

    # Assert
    # Check that metadata fields are correct
    for key in ['filename', 'filesize', 'checker', 'time', 'dictionary', 'errors']:
        print(key)
        assert response[key] == expected[key]


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
