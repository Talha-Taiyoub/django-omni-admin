from rest_framework import serializers

from community.models import Guest
from segment.models import Branch


class SimpleGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ["id", "name", "image"]


class VerySimpleBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name"]
