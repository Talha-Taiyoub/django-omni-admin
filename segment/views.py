from django.db.models import Count, IntegerField, OuterRef, Prefetch, Q, Subquery
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from general_app.format_response import (
    CustomResponseMixin,
    format_error_data,
    format_response_data,
)

from .models import (
    Booking,
    BookingItem,
    Branch,
    BranchSlider,
    Cart,
    CartItem,
    Destination,
    Room,
    RoomCategory,
)
from .paginations import CustomPagination
from .serializers import (
    BranchSerializer,
    BranchSliderSerializer,
    CartSerializer,
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
        # dates should be in YYYY-MM-DD format
        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")

        # Filter the bookings which are confirmed and overlap with user's check_in and check_out
        bookings = Booking.objects.filter(
            status__in=["Confirmed", "Checked In"]
        ).filter(check_in__lt=check_out, check_out__gt=check_in)

        # Find out the rooms that are already assigned
        assigned_rooms = (
            BookingItem.objects.filter(booking__in=bookings)
            .values_list("assigned_room", flat=True)
            .distinct()
        )

        # Filter out rooms that are not assigned and active
        room_queryset = Room.objects.exclude(id__in=assigned_rooms).filter(
            status="Active"
        )

        room_category_queryset = (
            RoomCategory.objects.filter(branch__id=branch_id)
            .filter(branch__status="Active")
            .filter(status="Active")
        )

        # Annotate available rooms count and exclude the room categories which have zero available room
        room_category_queryset = room_category_queryset.annotate(
            available_rooms_count=Count(
                "room",
                filter=Q(room__in=room_queryset),
            )
        ).filter(available_rooms_count__gt=0)

        # Include available rooms in the queryset
        # room_category_queryset = room_category_queryset.prefetch_related(
        #     Prefetch("room_set", queryset=room_queryset)
        # )

        queryset = (
            room_category_queryset.select_related("branch")
            .prefetch_related("room_amenities_set__amenity")
            .prefetch_related("gallery_set")
            .order_by("-discount_in_percentage")
        )
        return queryset

    serializer_class = RoomCategorySerializer
    pagination_class = CustomPagination
    list_message = "Fetched all the rooms that are available"
    retrieve_message = "Fetched the the room successfully."


class CartViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["post", "get"]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    create_message = "Cart is created successfully"
    retrieve_message = "The cart is fetched successfully"
