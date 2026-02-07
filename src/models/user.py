from django.contrib.auth.models import AbstractUser
from django.db import models

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

    class Meta:
        app_label = "users"   # 👈 tells Django this model belongs to the users app
