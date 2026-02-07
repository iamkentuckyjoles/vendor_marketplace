from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.api.v1.permissions import IsVerifier
from src.models.vendor import VendorApplication
from src.api.v1.schemas.vendor_schema import VendorApplicationSerializer
from django.utils.timezone import now

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
            elif action == "reject":
                application.status = "rejected"
                application.approved_at = now()
                application.approved_by = request.user
                application.rejection_reason = request.data.get("reason", "No reason provided")
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            application.save()
            serializer = VendorApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except VendorApplication.DoesNotExist:
            return Response({"error": "Vendor application not found"}, status=status.HTTP_404_NOT_FOUND)
