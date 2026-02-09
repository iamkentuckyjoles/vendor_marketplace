from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    ROLE_CHOICES = [
        ("new_user", "New User"),
        ("vendor", "Vendor"),
        ("verifier", "Verifier"),
        ("admin", "Admin"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ("username", "email", "role", "email_verified", "is_active", "is_staff")
    list_filter = ("role", "email_verified", "is_active", "is_staff")
    search_fields = ("username", "email")

    def save_model(self, request, obj, form, change):
        # If a raw password was entered, hash it before saving
        if "password" in form.cleaned_data:
            raw_password = form.cleaned_data["password"]
            if raw_password and not raw_password.startswith("pbkdf2_"):
                obj.set_password(raw_password)
        super().save_model(request, obj, form, change)

