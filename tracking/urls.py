from django.urls import path
from .views import goto_home

urlpatterns = [path("", goto_home, name="home")]
