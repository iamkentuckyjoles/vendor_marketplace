from django.urls import path, include

urlpatterns = [
    path("auth/", include("src.api.v1.routes.auth_urls")),
    path("user/", include("src.api.v1.routes.user_urls")),
    path("admin/", include("src.api.v1.routes.admin_urls")),
    path("vendor/", include("src.vendor.urls")),
    path("verifier/", include("src.api.v1.routes.verifier_urls")),
]
