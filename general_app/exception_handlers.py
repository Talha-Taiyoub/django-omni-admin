from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


# Created this so that The error message of invalid token will follow a format. Had to register this in the settings of REST_FRAMEWORK of settings.py file
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
