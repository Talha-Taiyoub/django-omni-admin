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


@admin.register(models.BranchStaff)
class BranchStaffAdmin(admin.ModelAdmin):
    list_display = ["id", "branch", "staff", "role", "date_joined"]
    list_select_related = ["branch", "staff"]

    def role(self, obj):
        return obj.staff.role


@admin.register(models.RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room_name",
        "status",
        "branch",
        "featured_image",
        "adults",
        "children",
        "regular_price",
        "discount_in_percentage",
        "created_at",
    ]

    list_select_related = ["branch"]


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room_category_name",
        "branch",
        "image",
    ]

    list_select_related = ["room_category", "room_category__branch"]

    def room_category_name(self, instance):
        return instance.room_category.room_name

    def branch(self, instance):
        return instance.room_category.branch.name


@admin.register(models.Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]


@admin.register(models.RoomAmenities)
class RoomAmenitiesAdmin(admin.ModelAdmin):
    list_display = ["id", "room_category_name", "branch", "amenity", "created_at"]

    list_select_related = ["room_category", "amenity", "room_category__branch"]

    def room_category_name(self, instance):
        return instance.room_category.room_name

    def branch(self, instance):
        return instance.room_category.branch.name


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "room_number", "room_category", "status", "created_at"]
    list_select_related = ["room_category", "room_category__branch"]


@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "full_name",
        "email",
        "mobile",
        "guest",
        "status",
        "check_in",
        "check_out",
        "placed_at",
    ]

    list_select_related = ["guest"]


@admin.register(models.BookingItem)
class BookingItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "booking_id",
        "room_category",
        "assigned_room",
        "price",
        "created_at",
    ]

    list_select_related = [
        "booking",
        "room_category__branch",
        "assigned_room__room_category__branch",
    ]

    def booking_id(self, instance):
        return instance.booking.id


@admin.register(models.Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "booking_id",
        "payment_status",
        "total",
        "discount",
        "subtotal",
        "paid",
        "total_due",
        "created_at",
    ]
    list_select_related = ["booking"]

    def booking_id(self, instance):
        return instance.booking.id


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "created_at"]
