from django.db.models import Count, Max, OuterRef, Prefetch, Q, Subquery
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from general_app.format_response import CustomResponseMixin, format_response_data

from .models import (
    Booking,
    BookingItem,
    Branch,
    BranchSlider,
    Cart,
    CartItem,
    Destination,
    Review,
    Room,
    RoomCategory,
    TouristSpot,
)
from .paginations import CustomPagination
from .serializers import (
    AddCartItemSerializer,
    BookingSerializer,
    BranchSerializer,
    BranchSliderSerializer,
    CartItemSerializer,
    CartSerializer,
    CreateBookingSerializer,
    DestinationSerializer,
    ReviewSerializer,
    RoomCategorySerializer,
    SpecialBranchSerializer,
    TouristSpotSerializer,
    UpdateCartItemSerializer,
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
    pagination_class = CustomPagination
    list_message = "Fetched all the branches successfully."
    retrieve_message = "Fetched the branch successfully."
    retrieve_error_message = "There is no branch listed with this id"

    @action(detail=False)
    def available(self, request):
        check_in = self.request.query_params.get("check_in")
        check_out = self.request.query_params.get("check_out")
        adults = self.request.query_params.get("adults")

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

        # Filter out the room categories which are active and have the same adults as adults in the query params
        room_category_queryset = RoomCategory.objects.filter(status="Active").filter(
            adults=int(adults)
        )

        # Annotate available rooms count and exclude the room categories which have zero available room
        room_category_queryset = room_category_queryset.annotate(
            available_rooms_count=Count(
                "room",
                filter=Q(room__in=room_queryset),
            )
        ).filter(available_rooms_count__gt=0)

        # Filter out the branches which are active
        branch_queryset = Branch.objects.filter(status="Active")

        # Keep only the branches which have at least one available room category for booking
        branch_queryset = branch_queryset.annotate(
            available_room_categories_count=Count(
                "roomcategory", filter=Q(roomcategory__in=room_category_queryset)
            )
        ).filter(available_room_categories_count__gt=0)

        # Include the room categories which are available in each branch
        branch_queryset = branch_queryset.prefetch_related(
            Prefetch("roomcategory_set", room_category_queryset)
        )

        # Subquery to find the maximum discount for the filtered room categories
        max_discount_subquery = (
            room_category_queryset.filter(branch_id=OuterRef("pk"))
            .values("branch")
            .annotate(max_discount=Max("discount_in_percentage"))
            .values("max_discount")
        )

        # Annotate branches with the maximum discount of their filtered room categories
        branch_queryset = branch_queryset.annotate(
            discount=Subquery(max_discount_subquery)
        ).order_by("-discount")

        queryset = branch_queryset.select_related("destination")

        # paginated queryset:
        page = self.paginate_queryset(queryset)
        serializer = SpecialBranchSerializer(page, many=True)
        response = self.get_paginated_response(serializer.data)
        custom_response = format_response_data(
            message=self.list_message,
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)


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
        adults = self.request.query_params.get("adults")

        if check_in and check_out and adults:
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
                .filter(adults=int(adults))
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
        else:
            queryset = (
                RoomCategory.objects.filter(branch__id=branch_id)
                .filter(branch__status="Active")
                .filter(status="Active")
                .annotate(
                    available_rooms_count=Count("room", filter=Q(room__status="Active"))
                )
                .order_by("-discount_in_percentage")
            )
        return queryset

    serializer_class = RoomCategorySerializer
    pagination_class = CustomPagination
    list_message = "Fetched all the rooms that are available"
    retrieve_message = "Fetched the the room successfully."
    retrieve_error_message = "There is no room listed with this id in this branch"


class CartViewSet(
    CustomResponseMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    http_method_names = ["post", "get", "delete"]
    queryset = Cart.objects.all().prefetch_related("items__room_category")
    serializer_class = CartSerializer

    create_message = "Cart is created successfully"
    retrieve_message = "The cart is fetched successfully"
    retrieve_error_message = "No cart is found with this id"
    delete_message = "The cart is deleted successfully"


class CartItemViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_pk")
        queryset = CartItem.objects.filter(cart__id=cart_id).select_related(
            "room_category"
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}

    create_message = "The room is added to the cart successfully"
    update_message = "The quantity is updated successfully"
    delete_message = "The room is removed from the cart successfully"
    retrieve_error_message = "No cart item is found with this id"
    post_create_and_post_update_serializer = CartItemSerializer


class BookingViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        guest = self.request.user.guest
        queryset = (
            Booking.objects.filter(guest_id=guest.id)
            .select_related("branch", "billing")
            .prefetch_related(
                "bookingitem_set__room_category", "bookingitem_set__assigned_room"
            )
            .order_by("-placed_at")
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBookingSerializer
        return BookingSerializer

    create_message = "We've received your booking request. You will get a call from our staff very soon."
    list_message = "All the bookings are fetched successfully"
    retrieve_message = "The booking is fetched successfully"
    retrieve_error_message = "This user has no booking with this booking id"
    post_create_and_post_update_serializer = BookingSerializer
    pagination_class = CustomPagination


class TouristSpotViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        branch_id = self.kwargs.get("branch_pk")
        queryset = TouristSpot.objects.filter(branch_id=branch_id).order_by(
            "distance_from_hotel_in_km"
        )
        return queryset

    serializer_class = TouristSpotSerializer
    pagination_class = CustomPagination
    list_message = "Fetched all the tourist spots successfully"
    retrieve_message = "Fetched the tourist spot successfully"
    retrieve_error_message = "There is no tourist spot listed with this id"


class ReviewViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = (
        Review.objects.all().select_related("guest").order_by("-rating", "-created_at")
    )
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    pagination_class = CustomPagination
    list_message = "All the reviews are fetched successfully"
    retrieve_message = "The review is fetched successfully"
    create_message = "The review is created successfully"
    retrieve_error_message = "There is no review listed with this id"
