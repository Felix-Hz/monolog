import logging
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ActivityForm
from .models import ActivityModel, ActivityExportModel
from .tasks import export_activity_task


def goto_home(request):
    activities = ActivityModel.objects.filter(user=request.user)
    last_export = (
        ActivityExportModel.objects.filter(user=request.user)
        .order_by("-exported_at")
        .first()
    )
    logging.debug(
        "Loaded home page",
        extra={
            "count": len(activities),
            "user_id": request.user.id,
            "has_last_export": bool(last_export),
        },
    )
    return render(
        request,
        "home.html",
        {
            "form": ActivityForm(),
            "activities": activities if activities else None,
            "last_export": last_export.file_path if last_export else None,
        },
    )


def create_activity(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            logging.info(
                "Succesfully created activity",
                extra={"user_id": request.user.id, "activity_id": activity.id},
            )
            return redirect("home")

    else:
        form = ActivityForm()

    return render(request, "home.html", {"form": form})


def delete_activity(request, activity_id):
    try:
        activity = ActivityModel.objects.get(id=activity_id, user=request.user)
        activity.delete()
        logging.info(
            "Successfully deleted activity",
            extra={"user_id": request.user.id, "activity_id": activity_id},
        )
    except ActivityModel.DoesNotExist:
        logging.warning(
            "Attempted to delete non-existent activity",
            extra={"activity_id": activity_id},
        )
    return redirect("home")


def export_activities(request):
    if request.method == "POST":
        user_id = request.user.id
        logging.info("Starting activities export", extra={"user_id": user_id})
        export_activity_task.delay(user_id)
        messages.success(
            request,
            "Export started successfully! Once it's ready, you'll receive it by email",
        )
    return redirect("home")
