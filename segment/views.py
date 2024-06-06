from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from general_app.format_response import format_response_data

from .models import Branch, Destination
from .serializers import BranchSerializer, DestinationSerializer


class DestinationViewSet(ModelViewSet):
    http_method_names = ["get"]
    queryset = Destination.objects.all().prefetch_related("branches")
    serializer_class = DestinationSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        custom_response = format_response_data(
            message="Fetched all the destinations successfully.",
            status_code=200,
            data=response.data,
        )
        return Response(custom_response, status=status.HTTP_200_OK)


class BranchViewSet(ModelViewSet):
    queryset = (
        Branch.objects.all().select_related("destination").prefetch_related("sliders")
    )
    serializer_class = BranchSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = serializer.save()
        serializer = BranchSerializer(branch)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
