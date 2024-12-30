from django.urls import include, re_path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
)

urlpatterns = [
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.social.urls")),
    re_path(r"^auth/", include("social_django.urls", namespace="social")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
    re_path(
        r"^auth/jwt/blacklist/", TokenBlacklistView.as_view(), name="jwt-blacklist"
    ),
]
