from django.urls import path
from .verifier_views import VendorReviewView

urlpatterns = [
    path("review-vendor/<int:vendor_id>/", VendorReviewView.as_view(), name="review_vendor"),
]
