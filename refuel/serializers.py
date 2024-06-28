# To avoid circular dependencies, we will not use anything in segment.serializer from this module
from rest_framework import serializers

from segment.models import Branch

from .models import Gallery, Reservation, Restaurant, RestaurantCuisine


class RestaurantCuisineSerializer(serializers.ModelSerializer):
    cuisine = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RestaurantCuisine
        fields = ["id", "cuisine"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "image"]


# I know I can inherit SimpleBranchSerializer from segments.serializer. But I want to keep it here.
class VerySimpleBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name"]


class RestaurantSerializer(serializers.ModelSerializer):
    branch = VerySimpleBranchSerializer(read_only=True)
    cuisines = RestaurantCuisineSerializer(many=True, read_only=True)
    gallery_set = GallerySerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "branch",
            "status",
            "overview",
            "featured_image",
            "gallery_set",
            "cuisines",
            "breakfast_opening",
            "breakfast_closing",
            "lunch_opening",
            "lunch_closing",
            "dinner_opening",
            "dinner_closing",
            "discount_in_percentage",
            "created_at",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(write_only=True)
    restaurant = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "name",
            "email",
            "mobile",
            "restaurant_id",
            "restaurant",
            "status",
            "number_of_people",
            "reservation_date",
            "reservation_time",
            "additional_information",
            "placed_at",
        ]
