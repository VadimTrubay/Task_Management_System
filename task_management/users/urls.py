from django.urls import path
from .views import SignupView, SigninView, LogoutView, UserDetailView

urlpatterns = [
    path("users/signup/", SignupView.as_view(), name="signup"),
    path("users/login/", SigninView.as_view(), name="login"),
    path("users/me/", UserDetailView.as_view(), name="me"),
    path("users/logout/", LogoutView.as_view(), name="logout"),
]
