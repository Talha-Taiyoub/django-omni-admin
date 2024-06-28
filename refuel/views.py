from rest_framework.viewsets import ModelViewSet

from general_app.format_response import CustomResponseMixin

from .models import Restaurant
from .serializers import RestaurantSerializer

# Create your views here.


class RestaurantViewSet(ModelViewSet):
    queryset = (
        Restaurant.objects.all()
        .select_related("branch")
        .prefetch_related("cuisines", "gallery_set")
    )
    serializer_class = RestaurantSerializer
