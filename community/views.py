from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from community.models import Guest
from community.serializers import GuestSerializer
from general_app.format_response import (
    format_error_data,
    format_response_data,
    format_validation_error,
)

# Create your views here.


class GuestViewSet(ModelViewSet):
    def handle_exception(self, exc):
        response = super().handle_exception(exc)

        # Check if the exception is a validation error
        if isinstance(exc, ValidationError):
            custom_response = format_validation_error(exc.detail)
            response = Response(custom_response, status=response.status_code)
        return response

    http_method_names = ["get", "put"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Guest.objects.filter(user=self.request.user).select_related("user")

    serializer_class = GuestSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        custom_response = format_response_data(
            message="Guest is fetched successfully.",
            data=serializer.data[0],
            status_code=200,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        custom_response = format_response_data(
            message="Guest is fetched successfully.",
            data=serializer.data,
            status_code=200,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if instance.user != request.user:
            custom_response = format_error_data(
                message="This is not your profile. You can't update or delete it",
                errors=[],
                status_code=400,
            )
            return Response(custom_response, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        custom_response = format_response_data(
            message="Profile has been updated successfully",
            status_code=200,
            data=serializer.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)
