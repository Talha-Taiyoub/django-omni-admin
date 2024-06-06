from rest_framework import serializers

from .models import Branch, BranchSlider, Destination


class SimpleDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "title"]


class BranchSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchSlider
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    sliders = BranchSliderSerializer(many=True, read_only=True)
    destination = SimpleDestinationSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = Branch
        fields = [
            "id",
            "name",
            "nick_name",
            "destination",
            "initial",
            "address",
            "status",
            "logo",
            "overview",
            "email",
            "telephone",
            "mobile",
            "location_iframe",
            "sliders",
            "created_at",
        ]

    # We kept this method here so that in future if we need any method like this, it can help us.
    # def create(self, validated_data):

    #     sliders = self.context["request"].FILES.getlist("sliders")
    #     branch = Branch.objects.create(**validated_data)

    #     for slider in sliders:
    #         Slider.objects.create(branch=branch, image=slider)

    #     return branch


class SimpleBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["id", "name", "address", "status", "logo"]


class DestinationSerializer(serializers.ModelSerializer):
    branches = SimpleBranchSerializer(many=True, read_only=True)

    class Meta:
        model = Destination
        fields = ["id", "title", "description", "image", "branches", "created_at"]
