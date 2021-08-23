"""Tests for API responses."""
from pathlib import Path
import re

from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from requests_toolbelt.multipart.encoder import MultipartEncoder

from app.main import app
from test.fixtures import ISVALID_RSP_DATA, VALIDATION_TEXT_RSP_DATA

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_openapi_json(client):
    """A hello-world type test to confirm testing framework works."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert '/validate' in response.text


@pytest.mark.parametrize('filename, expected', ISVALID_RSP_DATA)
@pytest.mark.asyncio
async def test_isvalid(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    mp_encoder = MultipartEncoder(
        fields={'file': (filename.name, open(filename, 'rb'), 'text/plain')})

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/isvalid/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == 1
    assert body['data'][0] == expected


@pytest.mark.xfail(reason="Will fail until text reponse is provided")
@pytest.mark.parametrize('filename, expected', VALIDATION_TEXT_RSP_DATA)
@pytest.mark.asyncio
async def test_validate_text(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    mp_encoder = MultipartEncoder(
        fields={'file': (filename.name, open(filename, 'rb'), 'text/plain')})
    expected_message, expected_size = expected

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/?fmt=text',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert f"File Name: \t {filename.name}" in response.text
    assert f"File Size: \t {expected_size:n} kB" in response.text
    assert re.search(expected_message, response.text)


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(app=app, base_url="http://test")
