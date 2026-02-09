from django.urls import path
from src.api.v1.routes.verifier_views import VendorReviewView
from .views import (
    VendorApplicationCreateView,
    VendorProductCreateView,
    VendorProductCreateView,
    VendorProductReviewView,
    VendorProductsByStatusView,
    VendorProductListView,
)



urlpatterns = [
    path("apply/", VendorApplicationCreateView.as_view(), name="vendor-apply"),
    path("review/<int:pk>/", VendorReviewView.as_view(), name="vendor-review"),
    path("products/<str:status_filter>/", VendorProductsByStatusView.as_view(), name="vendor_products_by_status"),
    path("products/submit/", VendorProductCreateView.as_view(), name="vendor_product_create"),
    path("products/<int:product_id>/review/", VendorProductReviewView.as_view(), name="vendor_product_review"),
    path("products/", VendorProductListView.as_view(), name="vendor_product_list"),
]
