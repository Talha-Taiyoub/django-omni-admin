from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()

router.register("restaurants", views.RestaurantViewSet, basename="restaurant")
router.register("reservations", views.ReservationViewSet, basename="reservation")
router.register("gyms", views.GymViewSet, basename="gym")

gym_router = NestedDefaultRouter(router, "gyms", lookup="gym")
gym_router.register("memberships", views.GymMembershipViewSet, basename="membership")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(gym_router.urls)),
]
