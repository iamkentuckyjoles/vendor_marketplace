from django.db import models
from django.conf import settings
from src.models.location import Region, Province, Municipality, Barangay

class VendorApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=255)
    store_name = models.CharField(max_length=255)

    # ✅ Allow nulls/blanks during development so migrations succeed
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, null=True, blank=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT, null=True, blank=True)
    barangay = models.ForeignKey(Barangay, on_delete=models.PROTECT, null=True, blank=True)

    contact_number = models.CharField(max_length=11)
    business_permit = models.ImageField(upload_to="permits/")
    google_maps_link = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    rejection_reason = models.TextField(blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="approved_vendors"
    )

    def __str__(self):
        return f"{self.store_name} ({self.applicant.username})"

    class Meta:
        app_label = "vendor"
