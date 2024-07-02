from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "branch",
        "status",
        "featured_image",
        "breakfast_opening",
        "breakfast_closing",
        "lunch_opening",
        "lunch_closing",
        "dinner_opening",
        "dinner_closing",
        "discount_in_percentage",
        "created_at",
    ]

    list_select_related = ["branch"]


@admin.register(models.Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]


@admin.register(models.RestaurantCuisine)
class RestaurantCuisineAdmin(admin.ModelAdmin):
    list_display = ["id", "restaurant", "cuisine"]
    list_select_related = ["restaurant", "cuisine"]


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "restaurant", "image"]
    list_select_related = ["restaurant"]


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "email",
        "mobile",
        "restaurant",
        "status",
        "number_of_people",
        "reservation_date",
        "reservation_time",
        "additional_information",
        "total_bill",
        "payment_status",
        "placed_at",
    ]

    list_select_related = ["restaurant"]


@admin.register(models.Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]


@admin.register(models.GymGender)
class GymGenderAdmin(admin.ModelAdmin):
    list_display = ["id", "gym", "gender", "created_at"]
    list_select_related = ["gym", "gender"]


@admin.register(models.GymGallery)
class GymGalleryAdmin(admin.ModelAdmin):
    list_display = ["id", "gym", "image"]
    list_select_related = ["gym"]


@admin.register(models.Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "branch",
        "status",
        "featured_image",
        "area",
        "fees",
        "opening",
        "closing",
        "discount_in_percentage",
        "created_at",
    ]

    list_select_related = ["branch"]


@admin.register(models.GymMembership)
class GymMembershipAdmin(admin.ModelAdmin):
    list_display = fields = [
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
    list_select_related = ["gym"]
