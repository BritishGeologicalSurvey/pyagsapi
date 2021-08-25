"""Tests for API responses."""
from pathlib import Path

from fastapi.testclient import TestClient
from freezegun import freeze_time
import pytest
from httpx import AsyncClient
from requests_toolbelt.multipart.encoder import MultipartEncoder

from app.main import app
from test.fixtures import FROZEN_TIME, ISVALID_RSP_DATA
from test.fixtures_json import JSON_RESPONSES
from test.fixtures_plain_text import PLAIN_TEXT_RESPONSES

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


@pytest.mark.parametrize('filename, expected',
                         [item for item in JSON_RESPONSES.items()])
@pytest.mark.asyncio
async def test_validate_json(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    mp_encoder = MultipartEncoder(
        fields={'file': (filename.name, open(filename, 'rb'), 'text/plain')})

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/',
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
    assert set(body['data'][0]) == set(expected.keys())
    assert body['data'][0]['filename'] == expected['filename']


@pytest.mark.asyncio
async def test_validatemany_json(async_client):
    # Arrange
    files = []
    for name in JSON_RESPONSES.keys():
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        files.append(file)
    mp_encoder = MultipartEncoder(fields=files)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validatemany/',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {'msg', 'type', 'self', 'data'}
    assert body['msg'] is not None
    assert body['type'] == 'success'
    assert body['self'] is not None
    assert len(body['data']) == len(JSON_RESPONSES)


@freeze_time(FROZEN_TIME)
@pytest.mark.parametrize('filename, expected',
                         [item for item in PLAIN_TEXT_RESPONSES.items()])
@pytest.mark.asyncio
async def test_validate_text(async_client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename
    mp_encoder = MultipartEncoder(
        fields={'file': (filename.name, open(filename, 'rb'), 'text/plain')})

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validate/?fmt=text',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    assert response.text.strip() == expected.strip()


@freeze_time(FROZEN_TIME)
@pytest.mark.asyncio
async def test_validatemany_text(async_client):
    # Arrange
    files = []
    for name in PLAIN_TEXT_RESPONSES.keys():
        filename = TEST_FILE_DIR / name
        file = ('files', (filename.name, open(filename, 'rb'), 'text/plain'))
        files.append(file)
    mp_encoder = MultipartEncoder(fields=files)

    # Act
    async with async_client as ac:
        response = await ac.post(
            '/validatemany/?fmt=text',
            headers={'Content-Type': mp_encoder.content_type},
            data=mp_encoder.to_string())

    # Assert
    assert response.status_code == 200
    for log in PLAIN_TEXT_RESPONSES.values():
        assert log.strip() in response.text


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(app=app, base_url="http://test")
