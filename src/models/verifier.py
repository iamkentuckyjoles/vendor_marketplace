# verifier/models.py
from django.db import models
from django.conf import settings
from src.vendor.models import VendorApplication
from src.location.models import Municipality, Barangay
from smart_selects.db_fields import ChainedManyToManyField

class VendorReview(models.Model):
    application = models.ForeignKey(VendorApplication, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    decision = models.CharField(max_length=20, choices=[("approved", "Approved"), ("rejected", "Rejected")])
    rejection_reason = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} reviewed {self.application} ({self.decision})"

    class Meta:
        app_label = "verifier"


class Verifier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_municipalities = models.ManyToManyField(Municipality, related_name="verifiers")
    assigned_barangays = models.ManyToManyField(Barangay, related_name="verifiers", blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Verifier: {self.user.username}"

    class Meta:
        app_label = "verifier"
