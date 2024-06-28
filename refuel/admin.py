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
