from rest_framework import generics
from .models import VendorApplication
from .serializers import VendorApplicationSerializer
from src.api.v1.services.permissions import IsNewUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.models.vendor import VendorProduct
from src.vendor.serializers import VendorProductSerializer
from django.utils.timezone import now
from src.api.v1.services.permissions import IsVendor, IsVerifier
from rest_framework.exceptions import ValidationError



class VendorApplicationCreateView(generics.CreateAPIView):
    queryset = VendorApplication.objects.all()
    serializer_class = VendorApplicationSerializer
    permission_classes = [IsNewUser]  # ✅ only new users can apply

    def perform_create(self, serializer):
        application = serializer.save(applicant=self.request.user, status="pending")
        # Optionally: promote user to 'vendor' immediately after applying
        self.request.user.role = "vendor"
        self.request.user.save()
        return application
    

class VendorApplicationsByStatusView(APIView):
    permission_classes = [IsVerifier]

    def get(self, request, status_filter):
        # Validate status_filter
        if status_filter not in ["pending", "approved", "rejected"]:
            return Response(
                {"error": "Invalid status. Use 'pending', 'approved', or 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        applications = VendorApplication.objects.filter(status=status_filter)
        serializer = VendorApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class VendorProductsByStatusView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        status_filter = self.kwargs.get("status_filter")
        if status_filter not in ["pending", "approved", "rejected"]:
            return VendorProduct.objects.none()
        # ✅ Only return products belonging to the logged-in vendor
        return VendorProduct.objects.filter(store__applicant=self.request.user, status=status_filter)



class VendorProductCreateView(generics.CreateAPIView):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer
    permission_classes = [IsVendor]

    def perform_create(self, serializer):
        # Find the vendor’s approved application
        try:
            store = VendorApplication.objects.get(applicant=self.request.user, status="approved")
        except VendorApplication.DoesNotExist:
            raise ValidationError("You must have an approved vendor application before posting products.")

        # Save product with auto‑linked store, municipality, barangay, and google maps
        serializer.save(
            store=store,
            municipality=store.municipality,
            barangay=store.barangay,
            google_maps_link=store.google_maps_link,
            status="pending"
        )


# ✅ Verifiers approve/reject products (APIView, custom logic)
class VendorProductReviewView(APIView):
    permission_classes = [IsVerifier]

    def post(self, request, product_id):
        try:
            product = VendorProduct.objects.get(id=product_id)
            action = request.data.get("action")  # "approve" or "reject"

            if action == "approve":
                product.status = "approved"
                product.approved_at = now()
                product.approved_by = request.user
                product.rejection_reason = None

            elif action == "reject":
                product.status = "rejected"
                product.approved_at = now()
                product.approved_by = request.user
                product.rejection_reason = request.data.get("reason", "No reason provided")

            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            product.save()
            serializer = VendorProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except VendorProduct.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class VendorProductListView(generics.ListAPIView):
    serializer_class = VendorProductSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        # Only return products belonging to the logged-in vendor
        return VendorProduct.objects.filter(store__applicant=self.request.user)




