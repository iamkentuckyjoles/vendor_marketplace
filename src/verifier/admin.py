from django.contrib import admin
from django import forms
from src.models.verifier import Verifier, VendorReview
from src.models.user import EmailVerificationCode, User
from src.models.location import Municipality, Barangay


@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "purpose", "created_at", "expires_at")
    list_filter = ("purpose", "expires_at")


class VerifierAdminForm(forms.ModelForm):
    class Meta:
        model = Verifier
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Only show users with role="verifier"
        self.fields["user"].queryset = User.objects.filter(role="verifier")

        # ✅ Handle municipalities from form data OR saved instance
        municipalities = None
        if "assigned_municipalities" in self.data:
            try:
                municipality_ids = self.data.getlist("assigned_municipalities")
                municipalities = Municipality.objects.filter(id__in=municipality_ids)
            except Exception:
                municipalities = None
        elif self.instance and self.instance.pk:
            municipalities = self.instance.assigned_municipalities.all()

        if municipalities and municipalities.exists():
            self.fields["assigned_barangays"].queryset = Barangay.objects.filter(
                municipality__in=municipalities
            )
        else:
            # Show all barangays so form validation doesn't fail
            self.fields["assigned_barangays"].queryset = Barangay.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        municipalities = cleaned_data.get("assigned_municipalities")
        barangays = cleaned_data.get("assigned_barangays")

        if municipalities and barangays:
            invalid = barangays.exclude(municipality__in=municipalities)
            if invalid.exists():
                raise forms.ValidationError(
                    f"These barangays are not in the selected municipalities: "
                    f"{', '.join(b.name for b in invalid)}"
                )
        return cleaned_data


@admin.register(Verifier)
class VerifierAdmin(admin.ModelAdmin):
    form = VerifierAdminForm
    list_display = ("user", "assigned_at")
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("assigned_municipalities", "assigned_barangays")


@admin.register(VendorReview)
class VendorReviewAdmin(admin.ModelAdmin):
    list_display = ("application", "reviewer", "decision", "reviewed_at")
    list_filter = ("decision", "reviewed_at")
