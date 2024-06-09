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
class BranchSliderViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]
    queryset = BranchSlider.objects.all().select_related("branch")
    serializer_class = BranchSliderSerializer
    list_message = "Fetched all the sliders for all the branches successfully."
    retrieve_message = "Fetched the slider successfully."


class RoomCategoryViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        branch_id = self.kwargs.get("branch_pk")
        queryset = (
            RoomCategory.objects.filter(branch__id=branch_id)
            .filter(branch__status="Active")
            .filter(status="Active")
        )

        # We will annotate room_count later which will be used to show how many rooms are left.
        queryset = (
            queryset.select_related("branch")
            .prefetch_related("room_amenities_set__amenity")
            .prefetch_related("gallery_set")
        )
        return queryset

    serializer_class = RoomCategorySerializer
    pagination_class = CustomPagination
    list_message = "Fetched all the rooms that are available"
    retrieve_message = "Fetched the the room successfully."
