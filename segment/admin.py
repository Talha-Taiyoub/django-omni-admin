from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "created_at"]
