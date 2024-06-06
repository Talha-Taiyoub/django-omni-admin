from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models

# Register your models here.


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "password",
        "is_active",
        "is_superuser",
        "is_staff",
        "last_login",
        "date_joined",
    ]
