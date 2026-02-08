from django.urls import path
from .auth import RegisterView, LoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from .auth import SendVerificationCodeView, VerifyCodeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("send-code/", SendVerificationCodeView.as_view(), name="send_code"), 
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),
]
