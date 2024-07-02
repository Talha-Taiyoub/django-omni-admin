from rest_framework import serializers

from community.models import Guest


class SimpleGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "name", "image"]
