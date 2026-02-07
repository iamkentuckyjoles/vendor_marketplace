from django.urls import path
from .users import UserProfileView

urlpatterns = [
    path("me/", UserProfileView.as_view(), name="user-profile"),
]
