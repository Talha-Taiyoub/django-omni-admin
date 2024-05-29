from rest_framework import serializers

from .models import Branch, Destination, Slider


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ["image"]


class BranchSerializer(serializers.ModelSerializer):
    sliders = SliderSerializer(many=True, required=False)
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

    def create(self, validated_data):
        sliders = validated_data.pop("sliders", [])
        branch = Branch.objects.create(**validated_data)

        for slider in sliders:
            Slider.objects.create(**slider, branch=branch)

        return branch
