import uuid
from django.conf import settings
from django.db import models


class ActivityStatus(models.TextChoices):
    PLANNED = "Planned"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class ActivityModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=200, blank=True)
    status = models.CharField(
        max_length=20, choices=ActivityStatus.choices, default=ActivityStatus.PLANNED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ActivityExportModel(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return "exports/user_{0}/{1}".format(instance.user.id, filename)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_ids = models.TextField(default=list, blank=True)
    exported_at = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f"Export {self.id} for {self.user.username} at {self.exported_at}"
