from django.urls import path
from .verifier_views import VendorReviewView, PendingVendorApplicationsView
from src.verifier.views import VerifierApplicationListView
from src.vendor.views import VendorApplicationsByStatusView
from src.verifier.views import (
    VerifierProductListView, 
    VerifierProductsByStatusView
)


urlpatterns = [
    path("pending-vendors/<int:vendor_id>/", VendorReviewView.as_view(), name="review_vendor"),
    path("pending-vendors/", PendingVendorApplicationsView.as_view(), name="pending_vendors"),
    path("applicants/", VerifierApplicationListView.as_view(), name="verifier_application_list"),
    path("applications/<str:status_filter>/", VendorApplicationsByStatusView.as_view(), name="vendor_applications_by_status"),
    path("products/", VerifierProductListView.as_view(), name="verifier_product_list"),
    path("products/<str:status_filter>/", VerifierProductsByStatusView.as_view(), name="vendor_products_by_status"),
]
