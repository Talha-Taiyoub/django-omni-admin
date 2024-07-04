from django.db import transaction
from rest_framework import serializers

from common_use.serializers import SimpleGuestSerializer

from .models import (
    Amenities,
    Billing,
    Booking,
    BookingItem,
    Branch,
    BranchSlider,
    Cart,
    CartItem,
    Destination,
    FavoriteRoomCategory,
    Gallery,
    Review,
    Room,
    RoomAmenities,
    RoomCategory,
    TouristSpot,
)


class SimpleDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "title"]


class BranchSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSlider
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    sliders = BranchSliderSerializer(many=True, read_only=True)
    destination = SimpleDestinationSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "nick_name",
            "destination",
            "initial",
            "address",
            "status",
            "logo",
            "overview",
            "email",
            "telephone",
            "mobile",
            "location_iframe",
            "sliders",
            "created_at",
        ]

    # We kept this method here so that in future if we need any method like this, it can help us.
    # def create(self, validated_data):

    #     sliders = self.context["request"].FILES.getlist("sliders")
    #     branch = Branch.objects.create(**validated_data)

    #     for slider in sliders:
    #         Slider.objects.create(branch=branch, image=slider)

    #     return branch


class SimpleBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "address", "status", "logo"]


class DestinationSerializer(serializers.ModelSerializer):
    branches = SimpleBranchSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = ["id", "title", "description", "image", "branches", "created_at"]


class RoomAmenitiesSerializer(serializers.ModelSerializer):
    amenity = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RoomAmenities
        fields = ["amenity"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["image"]


# Right now it's not used. But later we will use it if we need
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "status", "created_at"]


class RoomCategorySerializer(serializers.ModelSerializer):
    branch = SimpleBranchSerializer(read_only=True)
    room_amenities_set = RoomAmenitiesSerializer(many=True, read_only=True)
    gallery_set = GallerySerializer(many=True, read_only=True)
    available_rooms_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = RoomCategory
        fields = [
            "id",
            "room_name",
            "branch",
            "status",
            "featured_image",
            "overview",
            "gallery_set",
            "panorama",
            "room_amenities_set",
            "adults",
            "children",
            "regular_price",
            "discount_in_percentage",
            "available_rooms_count",
        ]


class SimpleRoomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = [
            "id",
            "room_name",
            "featured_image",
            "regular_price",
            "discounted_price",
        ]

    discounted_price = serializers.SerializerMethodField(
        method_name="get_discounted_price", read_only=True
    )

    def get_discounted_price(self, room_category):
        discount_amount = room_category.regular_price * (
            room_category.discount_in_percentage / 100
        )
        return room_category.regular_price - discount_amount


class FavoriteRoomCategorySerializer(serializers.ModelSerializer):
    room_category = RoomCategorySerializer(read_only=True)

    class Meta:
        model = FavoriteRoomCategory
        fields = ["id", "room_category"]


class CartItemSerializer(serializers.ModelSerializer):
    room_category = SimpleRoomCategorySerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "room_category",
            "quantity",
            "total_price",
        ]

    total_price = serializers.SerializerMethodField(
        method_name="get_total_price", read_only=True
    )

    def get_total_price(self, item: CartItem):
        discount_amount = item.room_category.regular_price * (
            item.room_category.discount_in_percentage / 100
        )
        discounted_price = item.room_category.regular_price - discount_amount
        return discounted_price * item.quantity


class AddCartItemSerializer(serializers.ModelSerializer):
    room_category_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "room_category_id", "quantity"]

    # Validating room_category_id that if it exists or not
    def validate_room_category_id(self, value):
        if not RoomCategory.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "No room category was found with this id."
            )
        return value

    def create(self, validated_data):
        cart_id = self.context["cart_id"]
        room_category_id = validated_data["room_category_id"]
        quantity = validated_data["quantity"]
        # At first, let's check same room_category is already listed under same cart or not?
        # If listed, we will just increase the quantity instead of creating another cart_item with the same cart and the same room category.
        try:
            cart_item = CartItem.objects.get(
                cart_id=cart_id, room_category_id=room_category_id
            )
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            # If not listed, we will create a new cart item.
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        return cart_item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price", "created_at"]

    total_price = serializers.SerializerMethodField(
        method_name="get_total_price", read_only=True
    )

    def get_total_price(self, cart):
        total_price = 0
        for item in cart.items.all():
            discount_amount = item.room_category.regular_price * (
                item.room_category.discount_in_percentage / 100
            )
            discounted_price = item.room_category.regular_price - discount_amount
            total_price += discounted_price * item.quantity
        return total_price


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ["id", "payment_status", "subtotal", "paid", "total_due"]


class BookingItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingItem
        fields = ["id", "room_category", "assigned_room", "price"]

    room_category = serializers.SerializerMethodField(method_name="get_room_category")
    assigned_room = serializers.SerializerMethodField(method_name="get_room_number")

    def get_room_category(self, instance: BookingItem):
        return instance.room_category.room_name

    def get_room_number(self, instance: BookingItem):
        return (
            instance.assigned_room.room_number
            if instance.assigned_room
            else "To be announced"
        )


class BookingSerializer(serializers.ModelSerializer):
    bookingitem_set = BookingItemSerializer(many=True, read_only=True)
    branch = serializers.StringRelatedField(read_only=True)
    billing = BillingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "full_name",
            "email",
            "mobile",
            "status",
            "check_in",
            "check_out",
            "branch",
            "additional_info",
            "placed_at",
            "bookingitem_set",
            "billing",
        ]


class CreateBookingSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(write_only=True)
    branch_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            "cart_id",
            "full_name",
            "email",
            "mobile",
            "check_in",
            "check_out",
            "branch_id",
            "additional_info",
        ]

    # The validate method is called after all the field validations is executed.
    # So don't worry about other validation logics that you defined in the fields of the model.
    def validate(self, data):
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        branch_id = data.get("branch_id")
        if check_out <= check_in:
            raise serializers.ValidationError(
                {"check_out": "Check out date must be greater than check in date"}
            )

        elif not Branch.objects.filter(pk=branch_id).exists():
            raise serializers.ValidationError(
                {"branch_id": "There is no branch with this id"}
            )
        return data

    def create(self, validated_data):
        guest = self.context["request"].user.guest
        cart_id = validated_data.pop("cart_id")

        # Check cart exists or not
        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            raise serializers.ValidationError(
                {"cart_id": "There is no cart with this id"}
            )

        cart_items = CartItem.objects.filter(cart_id=cart_id)
        if cart_items.count() < 1:
            raise serializers.ValidationError(
                {"cart_id": "There is no item in the cart"}
            )

        with transaction.atomic():
            booking = Booking.objects.create(guest=guest, **validated_data)
            booking_items = []
            total_price = 0  # We will use it in Billing object creation
            for item in cart_items:
                discount_amount = item.room_category.regular_price * (
                    item.room_category.discount_in_percentage / 100
                )
                discounted_price = item.room_category.regular_price - discount_amount
                total_price += discounted_price * item.quantity
                booking_items.extend(
                    [
                        BookingItem(
                            booking=booking,
                            room_category=item.room_category,
                            price=discounted_price,
                        )
                        for _ in range(item.quantity)
                    ]
                )

            BookingItem.objects.bulk_create(booking_items)
            Billing.objects.create(booking=booking, total=total_price)
            cart.delete()
            return booking


class TouristSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristSpot
        fields = [
            "id",
            "name",
            "branch_id",
            "distance_from_hotel_in_km",
            "featured_image",
            "created_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    guest = SimpleGuestSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "guest", "rating", "description", "created_at"]

    def create(self, validated_data):
        guest = self.context["request"].user.guest
        review = Review.objects.create(guest=guest, **validated_data)
        return review


class SpecialBranchSerializer(serializers.ModelSerializer):
    destination = SimpleDestinationSerializer(read_only=True)
    discount = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
    starts_from = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "nick_name",
            "destination",
            "initial",
            "address",
            "logo",
            "overview",
            "email",
            "telephone",
            "mobile",
            "discount",
            "starts_from",
        ]
