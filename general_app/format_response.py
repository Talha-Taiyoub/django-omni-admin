from rest_framework import status
from rest_framework.response import Response


# Method for formatting validation error response to our need
def format_validation_error(errors):
    formatted_errors = []
    for field, field_errors in errors.items():
        error_dict = {field: field_errors}
        formatted_errors.append(error_dict)
    return {
        "message": "Validation Error",
        "errors": formatted_errors,
        "status_code": 400,
        "success": False,
    }


# Method for formatting error data which are not validation errors
def format_error_data(message, errors, status_code):
    return {
        "message": message,
        "errors": errors,
        "status_code": status_code,
        "success": False,
    }


# Method for formatting response data
def format_response_data(message, data, status_code):
    return {
        "message": message,
        "data": data,
        "status_code": status_code,
        "success": True,
    }


# Class for overriding list and retrieve method of viewsets
class CustomResponseMixin:
    list_message = "All the items are fetched successfully"
    retrieve_message = "The item is fetched successfully"

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        custom_response = format_response_data(
            message=self.list_message,
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        custom_response = format_response_data(
            message=self.retrieve_message,
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)
