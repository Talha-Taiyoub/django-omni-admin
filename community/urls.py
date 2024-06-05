from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("guests", views.GuestViewSet, basename="guest")

urlpatterns = [path("", include(router.urls))]
