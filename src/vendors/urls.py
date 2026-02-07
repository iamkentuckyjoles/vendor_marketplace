from django.urls import path
from .views import VendorApplicationCreateView
from src.api.v1.routes.verifier_views import VendorReviewView

urlpatterns = [
    path("apply/", VendorApplicationCreateView.as_view(), name="vendor-apply"),
    path("review/<int:pk>/", VendorReviewView.as_view(), name="vendor-review"),
]
