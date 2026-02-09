from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import VendorReview
from .serializers import VendorReviewSerializer
from src.api.v1.services.permissions import IsVerifier
from src.models.vendor import VendorProduct
from src.vendor.serializers import VendorProductSerializer
from rest_framework.exceptions import ValidationError
from src.vendor.models import VendorApplication
from src.vendor.serializers import VendorApplicationSerializer


class VendorReviewView(generics.CreateAPIView):
    queryset = VendorReview.objects.all()
    serializer_class = VendorReviewSerializer
    permission_classes = [IsVerifier]

    def perform_create(self, serializer):
        serializer.save(
            reviewer=self.request.user,
            reviewed_at=timezone.now()
        )


class VerifierApplicationListView(generics.ListAPIView):
    serializer_class = VendorApplicationSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        # ✅ Show ALL vendor applications (pending, approved, rejected)
        return VendorApplication.objects.all()

# ✅ Verifiers can see all products
class VerifierProductListView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        # Option 1: show ALL products
        return VendorProduct.objects.all()


class PendingVendorProductsView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        return VendorProduct.objects.filter(status="pending")


class ApprovedVendorProductsView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        return VendorProduct.objects.filter(status="approved")


class RejectedVendorProductsView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        return VendorProduct.objects.filter(status="rejected")

class VerifierProductsByStatusView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVerifier]

    def get_queryset(self):
        status_filter = self.kwargs.get("status_filter")
        if status_filter not in ["pending", "approved", "rejected"]:
            raise ValidationError("Invalid status. Use 'pending', 'approved', or 'rejected'.")
        return VendorProduct.objects.filter(status=status_filter)