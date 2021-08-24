"""Tests for API responses."""
from pathlib import Path
import re

from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from requests_toolbelt.multipart.encoder import MultipartEncoder

from app.main import app

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_openapi_json(client):
    """A hello-world type test to confirm testing framework works."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert '/validate' in response.text


@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', True),
    ('nonsense.ags', False),
    ('empty.ags', False),
    ('real/A3040_03.ags', False),
    ('example1.xlsx', False),
    ('random_binary.ags', False),
    ('real/CG014058_F.ags', False),
    ('real/Blackburn Southern Bypass.ags', False),  # this file contains BOM character
])
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
@pytest.mark.parametrize('filename, expected', [
    ('example1.ags', 'All checks passed!'),
    ('nonsense.ags', r'7 error\(s\) found in file!'),
    ('empty.ags', r'4 error\(s\) found in file!'),
    ('real/A3040_03.ags', r'5733 error\(s\) found in file!'),
    ('example1.xlsx', 'ERROR: Only .ags files are accepted as input.'),
    ('random_binary.ags', 'ERROR: Unreadable character "á" at position 1 on line: 1\nStarting:'),
    ('real/CG014058_F.ags', r'ERROR: Unreadable character "æ" at position 80 on line: 263'),
    ('real/Blackburn Southern Bypass.ags', r'93 error\(s\) found in file!'),  # this file contains BOM character
])
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
    assert re.search(expected, response.text)


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function")
def async_client():
    return AsyncClient(app=app, base_url="http://test")
