from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.api.v1.permissions import IsAdmin
from src.api.v1.schemas.user_schema import VerifierCreateSerializer

from src.models.vendor import VendorApplication
from src.api.v1.schemas.vendor_schema import VendorApplicationSerializer

class CreateVerifierView(APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        serializer = VerifierCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"Verifier {user.username} created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorApplicationListView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        applications = VendorApplication.objects.all()
        serializer = VendorApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
