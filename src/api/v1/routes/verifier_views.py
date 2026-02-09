from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from src.api.v1.services.permissions import IsVerifier
from src.vendor.models import VendorApplication
from src.models.verifier import VendorReview
from src.verifier.serializers import VendorReviewSerializer
from src.vendor.serializers import VendorApplicationSerializer, VendorProductSerializer

from rest_framework.exceptions import ValidationError
from src.models.vendor import VendorProduct
from src.api.v1.services.permissions import IsVerifier

class VendorReviewView(APIView):
    permission_classes = [IsVerifier]

    def get(self, request, vendor_id):
        """View details of a specific vendor application"""
        try:
            application = VendorApplication.objects.get(id=vendor_id)
            serializer = VendorApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except VendorApplication.DoesNotExist:
            return Response({"error": "Vendor application not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, vendor_id):
        """Approve or reject a specific vendor application"""
        try:
            application = VendorApplication.objects.get(id=vendor_id)
            action = request.data.get("action")  # "approve" or "reject"

            if action == "approve":
                application.status = "approved"
                application.approved_at = now()
                application.approved_by = request.user
                application.rejection_reason = None
                # promote applicant to vendor role
                application.applicant.role = "vendor"
                application.applicant.save()
                decision = "approved"

            elif action == "reject":
                application.status = "rejected"
                application.approved_at = now()
                application.approved_by = request.user
                application.rejection_reason = request.data.get("reason", "No reason provided")
                decision = "rejected"

            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            application.save()

            # ✅ Create a review record
            review = VendorReview.objects.create(
                application=application,
                reviewer=request.user,
                decision=decision,
                rejection_reason=application.rejection_reason,
            )

            serializer = VendorReviewSerializer(review)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except VendorApplication.DoesNotExist:
            return Response({"error": "Vendor application not found"}, status=status.HTTP_404_NOT_FOUND)

class PendingVendorApplicationsView(APIView):
    permission_classes = [IsVerifier]

    def get(self, request):
        applications = VendorApplication.objects.filter(status="pending")
        serializer = VendorApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VendorProductReviewView(APIView):
    permission_classes = [IsVerifier]

    def post(self, request, pk):
        try:
            product = VendorProduct.objects.get(pk=pk, status="pending")
        except VendorProduct.DoesNotExist:
            raise ValidationError("Product not found or not pending.")

        action = request.data.get("action")
        reason = request.data.get("rejection_reason", "")

        if action == "approve":
            product.status = "approved"
            product.approved_by = request.user
            product.approved_at = timezone.now()
            product.rejection_reason = None
        elif action == "reject":
            product.status = "rejected"
            product.approved_by = request.user
            product.approved_at = timezone.now()
            product.rejection_reason = reason
        else:
            raise ValidationError("Invalid action. Use 'approve' or 'reject'.")

        product.save()
        return Response(VendorProductSerializer(product).data, status=status.HTTP_200_OK)
