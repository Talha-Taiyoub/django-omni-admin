from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()

router.register("restaurants", views.RestaurantViewSet, basename="restaurant")

urlpatterns = [path("", include(router.urls))]
