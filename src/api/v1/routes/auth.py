from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

from src.api.v1.schemas.user_schema import UserRegisterSerializer, UserLoginSerializer
from src.api.v1.services.auth_service import AuthService, send_verification_code
from src.models.user import User, EmailVerificationCode


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = AuthService.register_user(serializer.validated_data)
            # ✅ Require verification before login
            user.is_active = False
            user.email_verified = False
            user.role = "new_user"
            user.save()

            # ✅ Send code immediately after registration
            send_verification_code(user, purpose="register")

            return Response(
                {"message": "User registered successfully. Verification code sent."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # ✅ Enforce email verification
            if not user.email_verified:
                return Response({"error": "Email not verified"}, status=status.HTTP_403_FORBIDDEN)

            tokens = AuthService.login_user(serializer.validated_data)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        purpose = request.data.get("purpose", "register")

        try:
            user = User.objects.get(email=email)
            send_verification_code(user, purpose)
            return Response({"message": "Verification code sent"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        purpose = request.data.get("purpose", "register")

        try:
            user = User.objects.get(email=email)
            record = EmailVerificationCode.objects.filter(user=user, purpose=purpose).latest("created_at")

            if record.expires_at < timezone.now():
                return Response({"error": "Code expired"}, status=status.HTTP_400_BAD_REQUEST)
            if record.code != code:
                return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Mark user as verified
            user.email_verified = True
            user.is_active = True
            user.save()

            return Response({"message": "Code verified successfully"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except EmailVerificationCode.DoesNotExist:
            return Response({"error": "No code found"}, status=status.HTTP_404_NOT_FOUND)
