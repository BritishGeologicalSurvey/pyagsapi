"""Test for openapi responses."""


def test_openapi_json(client):
    """ Check that the openapi is accessible and it display the correct endpoints """
    response = client.get('/openapi.json')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'
    # exposed endpoints
    assert '/validate' in response.text
    assert '/convert' in response.text
    assert '/ags_log' in response.text
    assert '/ags_export' in response.text
    assert '/ags_export_by_polygon' in response.text
