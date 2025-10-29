from django.urls import path, include
from .views import SignUpView

urlpatterns = [
    path("", include("django.contrib.auth.urls")),  # ログイン等
    path("signup/", SignUpView.as_view(), name="signup"),
]
