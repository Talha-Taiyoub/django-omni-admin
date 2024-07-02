from rest_framework import serializers

from common_use.serializers import VerySimpleBranchSerializer

from .models import (
    Gallery,
    Gender,
    Gym,
    GymGallery,
    GymGender,
    Reservation,
    Restaurant,
    RestaurantCuisine,
)


class RestaurantCuisineSerializer(serializers.ModelSerializer):
    cuisine = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RestaurantCuisine
        fields = ["id", "cuisine"]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "image"]


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

    def validate_restaurant_id(self, value):
        if not Restaurant.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no restaurant with this id")
        return value


class GymGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = GymGallery
        fields = ["id", "image"]


class GymGenderSerializer(serializers.ModelSerializer):
    gender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GymGender
        fields = ["id", "gender"]


class GymSerializer(serializers.ModelSerializer):
    branch = VerySimpleBranchSerializer(read_only=True)
    gallery = GymGallerySerializer(many=True, read_only=True)
    gender_allowance = GymGenderSerializer(many=True, read_only=True)

    class Meta:
        model = Gym
        fields = [
            "id",
            "name",
            "branch",
            "status",
            "featured_image",
            "overview",
            "gallery",
            "gender_allowance",
            "area",
            "fees",
            "opening",
            "closing",
            "discount_in_percentage",
            "created_at",
        ]
