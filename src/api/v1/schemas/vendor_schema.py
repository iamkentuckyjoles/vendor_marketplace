from rest_framework import serializers
from src.models.vendor import VendorApplication

class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = [
            "id", "owner_name", "store_name", "location", "contact_number",
            "business_permit", "google_maps_link", "status", "rejection_reason",
            "submitted_at", "approved_at", "approved_by"
        ]
        read_only_fields = ["submitted_at", "approved_at", "approved_by"]
