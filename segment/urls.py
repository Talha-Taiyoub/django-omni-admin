from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
# We don't want to make destinations/destination_pk/branches because later it will be too nested. So we want to keep these separate
router.register("destinations", views.DestinationViewSet, basename="destination")
router.register("branches", views.BranchViewSet, basename="branch")
router.register("branch_sliders", views.BranchSliderViewSet, basename="branch_slider")
router.register("carts", views.CartViewSet, basename="cart")
router.register("bookings", views.BookingViewSet, basename="booking")

branch_router = NestedDefaultRouter(router, "branches", lookup="branch")
branch_router.register(
    "room_categories", views.RoomCategoryViewSet, basename="room_category"
)

branch_router.register(
    "tourist_spots", views.TouristSpotViewSet, basename="tourist_spot"
)

cart_router = NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("cartitems", views.CartItemViewSet, basename="cart_item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(branch_router.urls)),
    path("", include(cart_router.urls)),
]
