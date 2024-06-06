from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
# We don't want to make destinations/destination_pk/branches because later it will be too nested. So we want to keep these separate
router.register("destinations", views.DestinationViewSet, basename="destination")
router.register("branches", views.BranchViewSet, basename="branch")


urlpatterns = [path("", include(router.urls))]
