from rest_framework.viewsets import ModelViewSet

from general_app.format_response import CustomResponseMixin

from .models import Restaurant
from .paginations import CustomPagination
from .serializers import RestaurantSerializer

# Create your views here.


class RestaurantViewSet(CustomResponseMixin, ModelViewSet):
    http_method_names = ["get"]

    def get_queryset(self):
        branch_id = self.request.query_params.get("branch_id")
        print("IM HERE", branch_id)
        queryset = (
            Restaurant.objects.filter(status="Active")
            .select_related("branch")
            .prefetch_related("cuisines__cuisine", "gallery_set")
        )

        if branch_id is not None:
            queryset = queryset.filter(branch_id=branch_id)

        return queryset

    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination
    list_message = "All the restaurants are fetched successfully"
    retrieve_message = "The restaurant is fetched successfully"
    retrieve_error_message = "There is no restaurant with this id"
