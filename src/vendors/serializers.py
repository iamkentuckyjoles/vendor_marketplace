from rest_framework import serializers
from .models import VendorApplication

class VendorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorApplication
        fields = "__all__"
        # ✅ These fields are controlled by the system/verifier, not the vendor
        read_only_fields = [
            "status",
            "submitted_at",
            "approved_at",
            "approved_by",
            "rejection_reason",
        ]
