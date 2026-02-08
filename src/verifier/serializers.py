from rest_framework import serializers
from .models import VendorReview

class VendorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorReview
        fields = "__all__"
        read_only_fields = ["reviewer", "reviewed_at"]
