from fastapi import status
from starlette.requests import Request

from app.schemas import Error, ErrorResponse


# Define error responses
error_responses = {
    status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
    status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": ErrorResponse},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}
}


class HTTPExceptionResponse:
    def __init__(self, request: Request, exc: Exception):
        self.request = request
        self.exc = exc

    def response(self):
        response_data = {
            'msg': 'Not found',
            'type': 'bad request',
            'self': str(self.request.url),
            'errors': []
        }

        error_data = {
            'error': 'Bad request',
            'desc': 'Unknown Error'
        }

        if isinstance(self.exc.detail, dict):
            response_data['msg'] = self.exc.detail.get('msg', 'Unknown Error')
            error_data['error'] = self.exc.detail.get('error', 'Unknown Error')
            error_data['desc'] = self.exc.detail.get('desc', 'Unknown Error')
        else:
            error_data['desc'] = str(self.exc.detail)

        error = Error(**error_data)
        response_data['errors'].append(error)

        response = ErrorResponse(**response_data)
        return response


class InvalidPayloadError(Exception):
    def __init__(self, request: Request):
        self.request = request

    def response(self):
        response_data = {
            'msg': 'Invalid payload',
            'type': 'bad request',
            'self': str(self.request.url),
            'errors': []
        }

        error_data = {
            'error': 'Invalid payload',
            'desc': 'Please select at least one file and at least one checker',
        }
        error = Error(**error_data)
        response_data['errors'].append(error)

        response = ErrorResponse(**response_data)
        return response
