from rest_framework import serializers
from .models import VendorApplication
from src.location.models import Region, Province, Municipality, Barangay

class VendorApplicationSerializer(serializers.ModelSerializer):
    # Override FK fields to use names instead of IDs
    region = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Region.objects.all()
    )
    province = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Province.objects.all()
    )
    municipality = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Municipality.objects.all()
    )
    barangay = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Barangay.objects.all()
    )

    class Meta:
        model = VendorApplication
        fields = "__all__"
        read_only_fields = [
            "status",
            "submitted_at",
            "approved_at",
            "approved_by",
            "rejection_reason",
        ]

    # ✅ Cascading validation
    def validate(self, data):
        region = data.get("region")
        province = data.get("province")
        municipality = data.get("municipality")
        barangay = data.get("barangay")

        if province and region and province.region != region:
            raise serializers.ValidationError(
                {"province": f"{province.name} does not belong to {region.name}"}
            )
        if municipality and province and municipality.province != province:
            raise serializers.ValidationError(
                {"municipality": f"{municipality.name} does not belong to {province.name}"}
            )
        if barangay and municipality and barangay.municipality != municipality:
            raise serializers.ValidationError(
                {"barangay": f"{barangay.name} does not belong to {municipality.name}"}
            )

        return data
