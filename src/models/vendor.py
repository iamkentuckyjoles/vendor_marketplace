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


class VendorProduct(models.Model):
    CATEGORY_CHOICES = [
        ("meat", "Meat"),
        ("fruit", "Fruit"),
        ("vegetable", "Vegetable"),
        ("fish", "Fish"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    UNIT_CHOICES = [
        ("kg", "Per Kilo"),
        ("piece", "Per Piece"),
        ("bundle", "Per Bundle"),
        ("pack", "Per Pack"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_unit = models.CharField(max_length=20, choices=UNIT_CHOICES, default="kg")  # ✅ new field

    store = models.ForeignKey(VendorApplication, on_delete=models.CASCADE, related_name="products")
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    barangay = models.ForeignKey(Barangay, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    google_maps_link = models.URLField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_products"
    )
    rejection_reason = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to="products/", blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} ({self.get_category_display()}) - {self.store.store_name}"
    
    class Meta:
        app_label = "vendor"
