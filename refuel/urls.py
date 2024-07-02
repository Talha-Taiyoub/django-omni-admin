from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()

router.register("restaurants", views.RestaurantViewSet, basename="restaurant")
router.register("reservations", views.ReservationViewSet, basename="reservation")
router.register("gyms", views.GymViewSet, basename="gym")

urlpatterns = [path("", include(router.urls))]
