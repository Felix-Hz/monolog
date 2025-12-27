import logging
from functools import partial
from enum import StrEnum
from datetime import datetime
from celery import shared_task
import pandas as pd
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from .utils import setup_email
from .models import ActivityModel, ActivityExportModel


class ExportStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


@shared_task
def export_activity_task(user_id: int):
    try:
        activities = ActivityModel.objects.filter(user_id=user_id)
        logging.debug(
            "Exporting activities",
            extra={"count": activities.count(), "user_id": user_id},
        )

        df = pd.DataFrame.from_records(
            activities.values("id", "name", "description", "created_at")
        )
        csv_data = df.to_csv(index=False)

        export = ActivityExportModel(
            user=get_user_model().objects.get(id=user_id),
            activity_ids=list(activities.values_list("id", flat=True)),
        )

        filename = f"activities_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        # write csv data to the FileField
        export.file_path.save(
            filename, ContentFile(csv_data.encode("utf-8")), save=False
        )

        # save export, file field will automagically upload the file
        export.save()

        logging.info(
            "Successfully created export", extra={"user_id": user_id, "export": export}
        )

        send_export_email.delay(user_id, ExportStatus.SUCCESS, str(export.id))

        return (export.id, ExportStatus.SUCCESS)

    except Exception as e:
        logging.error(
            "Something went wrong during the activity export",
            extra={"user_id": user_id, "error": e},
        )

        send_export_email.delay(user_id, ExportStatus.FAILURE)

        return (export.id, ExportStatus.FAILURE)


@shared_task
def send_export_email(
    user_id: int,
    status: ExportStatus,
    export_id: str | None,
):
    try:
        user = get_user_model().objects.get(id=user_id)
        create_email = partial(setup_email, to_=user.email)

        if status == ExportStatus.SUCCESS and export_id is not None:
            export = ActivityExportModel.objects.get(id=export_id)

            # grab file contents
            export.file_path.open("r")
            csv_data = export.file_path.read()
            export.file_path.close()

            email = create_email(
                subject="Your Activity Export is Ready",
                body=f"Hi {user.username},\n\nYour export is attached.",
            )
            email.attach(export.file_path.name, csv_data, "text/csv")

        else:
            email = create_email(
                subject="Activity Export Failed",
                body=f"Hi {user.username},\n\nUnfortunately, your activity export failed. Please try again later.",
            )

        email.send()

        logging.info(
            "Succesfully notified user",
            extra={"user_email": user.email, "export_id": export_id},
        )
        return True

    except Exception as e:
        logging.error(
            "Failed to notify user",
            extra={"user_email": user.email, "export_id": export_id, "error": e},
        )
        return False
