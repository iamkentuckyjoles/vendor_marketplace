from django.urls import path, include

urlpatterns = [
    path("auth/", include("src.api.v1.routes.auth_urls")),
    path("users/", include("src.api.v1.routes.user_urls")),
    path("admin/", include("src.api.v1.routes.admin_urls")),
    path("vendors/", include("src.vendors.urls")),
    path("verifier/", include("src.api.v1.routes.verifier_urls")),
]
