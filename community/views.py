from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from community.models import Guest
from community.serializers import GuestSerializer

# Create your views here.


class GuestViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    http_method_names = ["get", "patch"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Guest.objects.filter(user=self.request.user).select_related("user")

    serializer_class = GuestSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
