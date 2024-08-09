from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.exceptions import ValidationError
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


# Class for overriding list,retrieve,create and destroy methods of viewsets
class CustomResponseMixin:
    list_message = "All the items are fetched successfully"
    retrieve_message = "The item is fetched successfully"
    create_message = "The instance is created successfully"
    delete_message = "The instance is deleted successfully"
    update_message = "The instance is updated successfully"
    retrieve_error_message = "No object is found with this id"
    post_create_and_post_update_serializer = None

    def handle_exception(self, exc):
        # Call parent's handle_exception to get the standard error response
        response = super().handle_exception(exc)

        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            custom_response = format_error_data(
                message="Authentication credentials are not provided",
                errors=[{"Log_In": ["You need to log in first"]}],
                status_code=401,
            )
            return Response(custom_response, status=status.HTTP_401_UNAUTHORIZED)

        # Check if the exception is not found error
        elif isinstance(exc, Http404):
            custom_response = format_error_data(
                message=self.retrieve_error_message,
                errors=[{"pk": ["Invalid id"]}],
                status_code=404,
            )
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

        # Check if the exception is a validation error
        elif isinstance(exc, ValidationError):
            # Format the validation errors
            custom_response = format_validation_error(exc.detail)
            # Create a new response with the formatted validation errors
            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        custom_response = format_response_data(
            message=self.list_message,
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        custom_response = format_response_data(
            message=self.retrieve_message,
            status_code=200,
            data=serializer.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_instance = serializer.save()
        if self.post_create_and_post_update_serializer is not None:
            serializer = self.post_create_and_post_update_serializer(created_instance)
        custom_response = format_response_data(
            message=self.create_message, status_code=201, data=serializer.data
        )
        return Response(custom_response, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()
        if self.post_create_and_post_update_serializer is not None:
            serializer = self.post_create_and_post_update_serializer(updated_instance)
        custom_response = format_response_data(
            message=self.update_message, status_code=200, data=serializer.data
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        custom_response = format_response_data(
            message=self.delete_message, status_code=200, data={}
        )
        return Response(custom_response, status=status.HTTP_200_OK)
