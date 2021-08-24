"""Tests for schemas."""
import datetime as dt

import pytest
from pydantic.error_wrappers import ValidationError

from app.schemas import Validation
from .test_ags import JSON_RESPONSES


BROKEN_JSON_RESPONSES = [
    {
        'filename': 'nonsense.ags',
        'filesize': 9,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': 'Standard_dictionary_v4_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'Rule 2a': [{'line': 1,
                         'group': 'NONE',
                         'desc': ''}],
        }
    },
    {
        'filename': 'nonsense.ags',
        'filesize': 9,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': 'Standard_dictionary_v4_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'Rule 2a': [{'line': '*',
                         'group': '',
                         'desc': ''}],
        }
    },
    {
        'filename': 'nonsense.ags',
        'filesize': 9,
        'checker': 'python_ags4 v0.3.6',
        'dictionary': 'Standard_dictionary_v4_1.ags',
        'time': dt.datetime(2021, 8, 23, 14, 25, 43, tzinfo=dt.timezone.utc),
        'message': '7 error(s) found in file!',
        'errors': {
            'Rule 0': [{'line': 1,
                        'group': '',
                        'desc': ''}],
        }
    },
]


@pytest.mark.parametrize('filename, data',
                         [item for item in JSON_RESPONSES.items()])
def test_validation(filename, data):
    v = Validation(**data)
    assert filename.endswith(v.filename)


@pytest.mark.parametrize('data',
                         [item for item in BROKEN_JSON_RESPONSES])
def test_failed_validation(data):
    with pytest.raises(ValidationError):
        Validation(**data)
