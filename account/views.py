from smtplib import SMTPException

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.timezone import now
from djoser import signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

User = get_user_model()


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


class CustomUserViewSet(UserViewSet):
    def handle_exception(self, exc):
        # Call parent's handle_exception to get the standard error response
        response = super().handle_exception(exc)

        # Check if the exception is a validation error
        if isinstance(exc, ValidationError):
            # Format the validation errors
            custom_response = format_validation_error(exc.detail)
            # Create a new response with the formatted validation errors
            response = Response(custom_response, status=response.status_code)
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        custom_response = format_response_data(
            message="An email has been sent containing the activation link, kindly click on it.",
            data=serializer.data,
            status_code=201,
        )
        return Response(
            custom_response, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        # user saving,sending signal and sending email are within atomic block so that if any error occurs within this block, all the changes within this part will be rolled back
        with transaction.atomic():
            user.is_active = True
            user.save()

            signals.user_activated.send(
                sender=self.__class__, user=user, request=self.request
            )

            if settings.SEND_CONFIRMATION_EMAIL:
                context = {"user": user}
                to = [get_user_email(user)]
                try:
                    settings.EMAIL.confirmation(self.request, context).send(to)
                except SMTPException as e:
                    custom_response = format_error_data(
                        message="Failed to send activation email. Please try again later.",
                        status_code=500,
                        errors=[],
                    )
                    return Response(
                        custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

        custom_response = format_response_data(
            message="Your account is activated, now you can log in.",
            status_code=200,
            data={},
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data["email"])
        except ObjectDoesNotExist:
            custom_response = format_error_data(
                message="There is no user found with this email. Register first.",
                status_code=404,
                errors=[],
            )
            return Response(custom_response, status=status.HTTP_404_NOT_FOUND)

        if not settings.SEND_ACTIVATION_EMAIL:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            custom_response = format_error_data(
                message="This account is already activated. If you forgot your password, try Forgot Password option.",
                status_code=400,
                errors=[],
            )
            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

        else:
            context = {"user": user}
            to = [get_user_email(user)]
            try:
                settings.EMAIL.activation(self.request, context).send(to)
            except SMTPException as e:
                custom_response = format_error_data(
                    message="Failed to send activation email. Please try again later.",
                    status_code=500,
                    errors=[],
                )
                return Response(
                    custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        custom_response = format_response_data(
            message="An email has been sent containing the activation link, kindly click on it.",
            data={},
            status_code=200,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    @action(["post"], detail=False)
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=serializer.data["email"])
        except User.DoesNotExist:
            custom_response = format_error_data(
                message="No account found with this email.", errors=[], status_code=404
            )
            return Response(
                custom_response,
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_active:
            context = {"user": user}
            to = [user.email]
            try:
                settings.EMAIL.password_reset(self.request, context).send(to)
            except SMTPException as e:
                custom_response = format_error_data(
                    message="Failed to send email. Please try again later.",
                    status_code=500,
                    errors=[],
                )
                return Response(
                    custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            custom_response = format_response_data(
                message="An email has been sent to your email address. Check the spam folder if necessary.",
                data={},
                status_code=200,
            )
            return Response(
                custom_response,
                status=status.HTTP_200_OK,
            )
        else:
            custom_response = format_error_data(
                message="The account is not active. To activate the account try 'Resend Activation' option.",
                status_code=400,
                errors=[],
            )
            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

    @action(["post"], detail=False)
    def reset_password_confirm(self, request, *args, **kwargs):

        if request.data["new_password"] != request.data["re_new_password"]:
            custom_response = format_error_data(
                message="Validation Error.",
                errors=[{"password": ["Passwords should match"]}],
                status_code=400,
            )
            return Response(
                custom_response,
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
            try:
                settings.EMAIL.password_changed_confirmation(
                    self.request, context
                ).send(to)
            except SMTPException as e:
                custom_response = format_error_data(
                    message="Failed to send the confirmation email.",
                    status_code=500,
                    errors=[],
                )
                return Response(
                    custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        custom_response = format_response_data(
            message="Password has been changed successfully.", data={}, status_code=200
        )
        return Response(
            custom_response,
            status=status.HTTP_200_OK,
        )

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            context = {"user": self.request.user}
            to = [get_user_email(self.request.user)]
            try:
                settings.EMAIL.password_changed_confirmation(
                    self.request, context
                ).send(to)
            except SMTPException as e:
                custom_response = format_error_data(
                    message="Failed to send confirmation email. Please try again later.",
                    status_code=500,
                    errors=[],
                )
                return Response(
                    custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        custom_response = format_response_data(
            message="You password is changed successfully", data={}, status_code=200
        )
        return Response(custom_response, status=status.HTTP_200_OK)
