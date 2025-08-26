import os

# Get AGS_API_ENV, defaults to DEVELOP if not set or not recognised.
AGS_API_ENV = os.getenv("AGS_API_ENV", "DEVELOP").upper()


def get_request_url(request):
    """ External calls need https to be returned, so check environment."""
    request_url = str(request.url)
    if AGS_API_ENV == 'PRODUCTION' and request_url.startswith('http:'):
        request_url = request_url.replace('http:', 'https:')

    return request_url
