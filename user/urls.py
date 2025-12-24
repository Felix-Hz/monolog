from django.urls import path
from .views import UserLoginView, UserSignupView, UserLogoutView

urlpatterns = [
    path("user/login/", UserLoginView.as_view(), name="login"),
    path("user/signup/", UserSignupView.as_view(), name="signup"),
    path("user/logout/", UserLogoutView.as_view(), name="logout"),
]
