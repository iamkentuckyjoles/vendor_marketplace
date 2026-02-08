from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("verifier", "Verifier"),
        ("vendor", "Vendor"),
        ("new_user", "New User"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="new_user")
    date_verified_vendor = models.DateTimeField(null=True, blank=True)
    account_expiry = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username"] 

    class Meta:
        app_label = "user"   # 👈 tells Django this model belongs to the users app

class EmailVerificationCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="verification_codes")
    code = models.CharField(max_length=6)  # short numeric or alphanumeric code
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    purpose = models.CharField(max_length=20, choices=[("register", "Register"), ("reset", "Reset Password")])

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.code} ({self.purpose})"

    class Meta:
        app_label = "user"   # ✅ tells Django this model belongs to the 'users' app
