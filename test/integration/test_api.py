"""Tests for API responses."""
from pathlib import Path
import re

from fastapi.testclient import TestClient
import pytest

from app.main import app

TEST_FILE_DIR = Path(__file__).parent.parent / 'files'


def test_openapi_json(client):
    """A hello-world type test to confirm testing framework works."""
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert '/validate' in response.text


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
def test_validate(client, filename, expected):
    # Arrange
    filename = TEST_FILE_DIR / filename

    # Act
    response = client.post('/validate/?fmt=text',
                           files={'file': (filename.name, str(filename))})

    # Assert
    assert response.status_code == 200
    assert re.search(expected, response.text)


@pytest.fixture(scope="function")
def client():
    return TestClient(app)
