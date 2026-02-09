# verifier/serializers.py
from rest_framework import serializers
from src.models.verifier import VendorReview

class VendorReviewSerializer(serializers.ModelSerializer):
    # ✅ Show reviewer details instead of just ID
    reviewer_username = serializers.CharField(source="reviewer.username", read_only=True)
    reviewer_email = serializers.EmailField(source="reviewer.email", read_only=True)

    class Meta:
        model = VendorReview
        fields = [
            "id",
            "decision",
            "rejection_reason",
            "reviewed_at",
            "application",
            "reviewer",           # keep raw ID if you want internal reference
            "reviewer_username",  # human-friendly username
            "reviewer_email",     # human-friendly email
        ]
