from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from general_app.format_response import (
    CustomResponseMixin,
    format_error_data,
    format_response_data,
)

from .models import Branch, BranchSlider, Destination, RoomCategory
from .paginations import CustomPagination
from .serializers import (
    BranchSerializer,
    BranchSliderSerializer,
    DestinationSerializer,
    RoomCategorySerializer,
)


class DestinationViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]
    queryset = Destination.objects.all().prefetch_related("branches")
    serializer_class = DestinationSerializer

    list_message = "All the destinations are fetched successfully."
    retrieve_message = "The destination is fetched successfully."


class BranchViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]
    queryset = (
        Branch.objects.all().select_related("destination").prefetch_related("sliders")
    )
    serializer_class = BranchSerializer

    list_message = "Fetched all the branches successfully."
    retrieve_message = "Fetched the branch successfully."


# Created this view so that the frontend dev can get all the sliders at once
class BranchSliderViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = BranchSlider.objects.all().select_related("branch")
    serializer_class = BranchSliderSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        custom_response = format_response_data(
            message="Fetched all the sliders for all the branches successfully.",
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        custom_response = format_response_data(
            message="Fetched the slider successfully.",
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)


class RoomCategoryViewSet(ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = RoomCategory.objects.filter(status="Active").filter(
            branch__status="Active"
        )

        branch_id = self.request.query_params.get("branch_id", None)
        if branch_id is not None:
            queryset = queryset.filter(branch__id=branch_id)

        # We will annotate room_count later which will be used to show how many rooms are left.
        queryset = (
            queryset.select_related("branch")
            .prefetch_related("room_amenities_set__amenity")
            .prefetch_related("gallery_set")
        )
        return queryset

    serializer_class = RoomCategorySerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # Paginate the queryset
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        paginated_response = self.get_paginated_response(serializer.data)
        custom_response = format_response_data(
            message="Fetched all the rooms that are available",
            status_code=200,
            data=paginated_response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        custom_response = format_response_data(
            message="Fetched the the room successfully.",
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)
