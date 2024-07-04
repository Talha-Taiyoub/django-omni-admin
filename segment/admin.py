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

    list_select_related = ["destination"]
    list_editable = ["status"]


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

    list_editable = ["status", "discount_in_percentage"]
    list_select_related = ["branch"]
    ordering = ["branch__name", "room_name", "status"]


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
    list_editable = ["status"]

    ordering = [
        "room_category__branch__name",
        "room_category__room_name",
        "room_number",
    ]


@admin.register(models.FavoriteRoom)
class FavoriteRoomAdmin(admin.ModelAdmin):
    list_display = ["id", "room_category", "created_at"]
    list_select_related = ["room_category", "room_category__branch"]
    ordering = ["room_category__branch__name", "room_category__room_name"]


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


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["id", "room_category", "quantity", "total_price", "cart"]
    list_select_related = ["room_category__branch", "cart"]

    def total_price(self, item):
        discount_amount = item.room_category.regular_price * (
            item.room_category.discount_in_percentage / 100
        )
        discounted_price = item.room_category.regular_price - discount_amount
        return discounted_price * item.quantity


@admin.register(models.TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "branch",
        "distance_from_hotel_in_km",
        "featured_image",
        "created_at",
    ]

    list_select_related = ["branch"]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "guest", "rating", "description", "created_at"]
    list_select_related = ["guest"]
