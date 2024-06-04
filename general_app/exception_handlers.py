from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
)
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, TokenError)):
        custom_response_data = {
            "message": "Given token is not valid or expired",
            "status_code": 401,
            "errors": [],
            "success": False,
        }
        response.data = custom_response_data

    return response
