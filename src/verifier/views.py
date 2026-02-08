from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import VendorReview
from .serializers import VendorReviewSerializer
from src.api.v1.services.permissions import IsVerifier

class VendorReviewView(generics.CreateAPIView):
    queryset = VendorReview.objects.all()
    serializer_class = VendorReviewSerializer
    permission_classes = [IsVerifier]

    def perform_create(self, serializer):
        serializer.save(
            reviewer=self.request.user,
            reviewed_at=timezone.now()
        )
