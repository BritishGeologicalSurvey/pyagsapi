"""Tests for schemas."""
import pytest
from pydantic import ValidationError

from app.schemas import Validation
from test.fixtures_json import JSON_RESPONSES, BROKEN_JSON_RESPONSES


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
