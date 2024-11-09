from rest_framework import serializers

from common_use.serializers import VerySimpleBranchSerializer

from .models import (
    Gallery,
    Gym,
    GymGallery,
    GymGender,
    GymMembership,
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
    breakfast_opening = serializers.SerializerMethodField()
    breakfast_closing = serializers.SerializerMethodField()
    lunch_opening = serializers.SerializerMethodField()
    lunch_closing = serializers.SerializerMethodField()
    dinner_opening = serializers.SerializerMethodField()
    dinner_closing = serializers.SerializerMethodField()

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

    def get_breakfast_opening(self, restaurant: Restaurant):
        return restaurant.breakfast_opening.strftime("%I:%M%p")

    def get_breakfast_closing(self, restaurant: Restaurant):
        return restaurant.breakfast_closing.strftime("%I:%M%p")

    def get_lunch_opening(self, restaurant: Restaurant):
        return restaurant.lunch_opening.strftime("%I:%M%p")

    def get_lunch_closing(self, restaurant: Restaurant):
        return restaurant.lunch_closing.strftime("%I:%M%p")

    def get_dinner_opening(self, restaurant: Restaurant):
        return restaurant.dinner_opening.strftime("%I:%M%p")

    def get_dinner_closing(self, restaurant: Restaurant):
        return restaurant.dinner_closing.strftime("%I:%M%p")


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
    opening = serializers.SerializerMethodField()
    closing = serializers.SerializerMethodField()

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

    def get_opening(self, gym: Gym):
        return gym.opening.strftime("%I:%M%p")

    def get_closing(self, gym: Gym):
        return gym.closing.strftime("%I:%M%p")


class GymMembershipSerializer(serializers.ModelSerializer):
    gym = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(max_length=15, read_only=True)
    monthly_fees = serializers.DecimalField(
        max_digits=9, decimal_places=2, read_only=True
    )

    class Meta:
        model = GymMembership
        fields = [
            "id",
            "gym",
            "status",
            "name",
            "gender",
            "age",
            "mobile",
            "email",
            "monthly_fees",
            "additional_info",
            "created_at",
        ]

    def create(self, validated_data):
        gym_id = self.context["gym_id"]

        try:
            gym = Gym.objects.get(pk=gym_id)
        except Gym.DoesNotExist:
            raise serializers.ValidationError(
                {"gym_id": ["There is no gym listed with this id"]}
            )

        discount_amount = gym.fees * (gym.discount_in_percentage / 100)
        discounted_fees = gym.fees - discount_amount

        membership = GymMembership.objects.create(
            monthly_fees=discounted_fees, gym=gym, **validated_data
        )
        return membership
