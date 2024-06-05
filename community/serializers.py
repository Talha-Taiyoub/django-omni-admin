from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Guest

User = get_user_model()


class SimpleUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


class GuestSerializer(serializers.ModelSerializer):
    user = SimpleUser(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Guest
        fields = [
            "id",
            "user",
            "name",
            "mobile",
            "status",
            "county",
            "state",
            "city",
            "postal_code",
            "image",
        ]
