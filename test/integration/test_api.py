"""Tests for API responses."""
from fastapi.testclient import TestClient
import pytest

from app.main import app


def test_openapi_json(client):
    """A hello-world type test to confirm testing framework works."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert '/validate' in response.text


@pytest.fixture(scope="function")
def client():
    return TestClient(app)
