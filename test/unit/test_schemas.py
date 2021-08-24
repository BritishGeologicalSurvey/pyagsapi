"""Tests for schemas."""
import pytest

from app.schemas import Validation
from .test_ags import JSON_RESPONSES


@pytest.mark.parametrize('filename, data',
                         [item for item in JSON_RESPONSES.items()])
def test_validation(filename, data):
    v = Validation(**data)
    assert v.filename == filename
