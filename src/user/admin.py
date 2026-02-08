from django.contrib import admin
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

# ✅ Custom form to make role a dropdown
class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

    ROLE_CHOICES = [
        ("user", "User"),
        ("verifier", "Verifier"),
        ("vendor", "Vendor"),
        ("admin", "Admin"),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email")
