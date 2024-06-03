# Writing views to override methods of Djoser's views
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

# This commented part works. We will use it to format response for validation error. We will understand it and then use it
# def format_validation_error(errors):
#     formatted_errors = {}
#     for field, field_errors in errors.items():
#         formatted_errors[field] = field_errors
#     return {"message": "Validation Error", "errors": formatted_errors}

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    # def handle_exception(self, exc):
    #     # Call parent's handle_exception to get the standard error response
    #     response = super().handle_exception(exc)

    #     # Check if the exception is a validation error
    #     if isinstance(exc, ValidationError):
    #         # Format the validation errors
    #         custom_response = format_validation_error(exc.detail)
    #         # Create a new response with the formatted validation errors
    #         response = Response(custom_response, status=response.status_code)

    #     return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "An email has been sent to your email with the activation link. Kindly click it",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data["email"])
        except User.DoesNotExist:
            return Response(
                {"message": "No account found with this email."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user:
            context = {"user": user}
            to = [user.email]
            settings.EMAIL.password_reset(self.request, context).send(to)
            return Response(
                {
                    "message": "An email has been sent to your email address. Check the spam folder if necessary"
                },
                status=status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):

        if request.data["new_password"] != request.data["re_new_password"]:
            return Response(
                {"message": "Passwords should match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.user.set_password(serializer.data["new_password"])
        if hasattr(serializer.user, "last_login"):
            serializer.user.last_login = now()
        serializer.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": serializer.user}
            to = [get_user_email(serializer.user)]
            settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
        return Response(
            {"message": "Password has been changed successfully."},
            status=status.HTTP_200_OK,
        )
