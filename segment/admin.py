from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "image", "created_at"]


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = [
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
        "created_at",
    ]


@admin.register(models.BranchSlider)
class BranchSliderAdmin(admin.ModelAdmin):
    list_display = ["id", "branch", "type", "featured_image"]
    list_select_related = ["branch"]
