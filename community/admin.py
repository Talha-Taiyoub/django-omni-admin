from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "name",
        "mobile",
        "status",
        "county",
        "state",
        "city",
        "postal_code",
        "image",
        "created_at",
    ]
    list_select_related = ["user"]


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "name",
        "mobile",
        "role",
        "county",
        "state",
        "city",
        "postal_code",
        "image",
        "created_at",
    ]
    list_select_related = ["user"]
