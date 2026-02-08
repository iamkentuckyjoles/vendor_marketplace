# verifier/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from src.api.v1.services.permissions import IsVerifier
from src.vendor.models import VendorApplication
from src.models.verifier import VendorReview
from src.verifier.serializers import VendorReviewSerializer

class VendorReviewView(APIView):
    permission_classes = [IsVerifier]

    def post(self, request, vendor_id):
        try:
            application = VendorApplication.objects.get(id=vendor_id)
            action = request.data.get("action")  # "approve" or "reject"

            if action == "approve":
                application.status = "approved"
                application.approved_at = now()
                application.approved_by = request.user
                application.rejection_reason = None
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
