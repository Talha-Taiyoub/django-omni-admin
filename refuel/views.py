from rest_framework.viewsets import ModelViewSet

from general_app.format_response import CustomResponseMixin

from .models import Restaurant
from .paginations import CustomPagination
from .serializers import RestaurantSerializer

# Create your views here.


class RestaurantViewSet(CustomResponseMixin, ModelViewSet):
    queryset = (
        Restaurant.objects.all()
        .select_related("branch")
        .prefetch_related("cuisines__cuisine", "gallery_set")
    )
    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination
    list_message = "All the restaurants are fetched successfully"
    retrieve_message = "The restaurant is fetched successfully"
    retrieve_error_message = "There is no restaurant with this id"
