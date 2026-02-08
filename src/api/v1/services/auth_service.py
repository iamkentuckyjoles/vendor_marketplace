from src.api.v1.utils.jwt_utils import generate_tokens
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail
from src.models.user import EmailVerificationCode

class AuthService:
    @staticmethod
    def register_user(data):
        from src.models.user import User
        return User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role=data.get("role", "new_user"),
        )

    @staticmethod
    def login_user(data):
        user = data["user"]
        return generate_tokens(user)


def send_verification_code(user, purpose="register"):
    # Generate a random 6-digit code
    code = str(random.randint(100000, 999999))
    expiry = timezone.now() + timedelta(minutes=10)

    # Save to DB
    verification = EmailVerificationCode.objects.create(
        user=user,
        code=code,
        expires_at=expiry,
        purpose=purpose,
    )

    # Send email
    send_mail(
        subject="Your Verification Code",
        message=f"Your code is {code}. It expires in 10 minutes.",
        from_email="no-reply@vendor-marketplace.com",
        recipient_list=[user.email],
    )

    return verification
