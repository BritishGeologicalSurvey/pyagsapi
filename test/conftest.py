"""Configuration for test fixtures."""
# The following line is required to allow Pandas to work with Freeze Gun.
# Without it, Pandas will throw an error.  See here for details:
# https://github.com/spulec/freezegun/issues/98
import pandas  # noqa

from fastapi.testclient import TestClient
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
