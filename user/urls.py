from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import UserLoginView, UserSignupView

urlpatterns = [
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/signup/", UserSignupView.as_view(), name="signup"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
]
