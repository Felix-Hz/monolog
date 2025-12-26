from django.contrib import admin
from .models import ActivityModel


@admin.register(ActivityModel)
class ActivityAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
