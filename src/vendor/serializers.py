from rest_framework import serializers
from .models import VendorApplication
from src.location.models import Region, Province, Municipality, Barangay
from src.models.vendor import VendorProduct

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

    # ✅ Add applicant details
    applicant_username = serializers.CharField(source="applicant.username", read_only=True)
    applicant_email = serializers.EmailField(source="applicant.email", read_only=True)

    class Meta:
        model = VendorApplication
        fields = "__all__"  # still include everything
        read_only_fields = [
            "status",
            "submitted_at",
            "approved_at",
            "approved_by",
            "rejection_reason",
            "applicant",
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


class VendorProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source="store.store_name", read_only=True)
    municipality_name = serializers.CharField(source="municipality.name", read_only=True)
    barangay_name = serializers.CharField(source="barangay.name", read_only=True)
    approved_by_username = serializers.SerializerMethodField()
    approved_by_email = serializers.SerializerMethodField()
    price_unit_display = serializers.CharField(source="get_price_unit_display", read_only=True)

    class Meta:
        model = VendorProduct
        fields = [
            "id",
            "category",
            "product_name",
            "price",
            "price_unit",
            "price_unit_display",
            "store",              # FK to VendorApplication
            "store_name",
            "municipality",
            "municipality_name",
            "barangay",
            "barangay_name",
            "street_address",
            "google_maps_link",
            "status",
            "submitted_at",
            "approved_at",
            "approved_by",
            "approved_by_username",
            "approved_by_email",
            "rejection_reason",
            "image",
        ]
        read_only_fields = [
            "store",              # ✅ now read-only
            "municipality",       # ✅ now read-only
            "barangay",           # ✅ now read-only
            "google_maps_link",   # ✅ now read-only
            "status",
            "submitted_at",
            "approved_at",
            "approved_by",
            "approved_by_username",
            "approved_by_email",
            "rejection_reason",
        ]

    def get_approved_by_username(self, obj):
        return obj.approved_by.username if obj.approved_by else "N/A"

    def get_approved_by_email(self, obj):
        return obj.approved_by.email if obj.approved_by else "N/A"
