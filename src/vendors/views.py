from rest_framework import generics
from .models import VendorApplication
from .serializers import VendorApplicationSerializer
from src.api.v1.permissions import IsNewUser

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
