from django.contrib import admin
from .models import VendorReview
from src.models.user import EmailVerificationCode
from src.models.verifier import Verifier

@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "purpose", "created_at", "expires_at")
    list_filter = ("purpose", "expires_at")

@admin.register(Verifier)
class VerifierAdmin(admin.ModelAdmin):
    list_display = ("user", "assigned_at")
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("assigned_barangays",) 

@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ("application", "reviewer", "decision", "reviewed_at")
    list_filter = ("decision", "reviewed_at")

