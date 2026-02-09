from django.contrib import admin
from src.vendor.models import VendorApplication

@admin.register(VendorApplication)
class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "store_name",
        "owner_name",
        "applicant",
        "municipality",   # ✅ show municipality
        "barangay",       # ✅ show barangay
        "status",
        "submitted_at",
        "approved_by_username",  # ✅ custom column
    )
    list_filter = ("status", "region", "province")
    search_fields = (
        "store_name",
        "owner_name",
        "applicant__username",
        "applicant__email",
        "municipality__name",
        "barangay__name",
    )

    # ✅ Custom method to display username of approved_by
    def approved_by_username(self, obj):
        if obj.approved_by:
            return obj.approved_by.username  # or obj.approved_by.email if you prefer
        return "-"
    approved_by_username.short_description = "Approved By"
