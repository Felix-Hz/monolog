from django.urls import path
from . import views

urlpatterns = [
    path("activity/create/", views.create_activity, name="create_activity"),
    path(
        "activity/delete/<uuid:activity_id>/",
        views.delete_activity,
        name="delete_activity",
    ),
    path("", views.goto_home, name="home"),
]
