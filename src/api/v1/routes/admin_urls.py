from django.urls import path
from .admin_views import CreateVerifierView, VendorApplicationListView

urlpatterns = [
    path("create-verifier/", CreateVerifierView.as_view(), name="create_verifier"),
    path("vendor-applications/", VendorApplicationListView.as_view(), name="vendor_applications"),
]
