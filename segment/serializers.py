from rest_framework import serializers

from .models import (
    Amenities,
    Branch,
    BranchSlider,
    Cart,
    CartItem,
    Destination,
    Gallery,
    Room,
    RoomAmenities,
    RoomCategory,
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


class CartItemSerializer(serializers.ModelSerializer):
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


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "created_at"]
