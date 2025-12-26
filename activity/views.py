import logging

from django.shortcuts import redirect, render
from .forms import ActivityForm
from .models import ActivityModel


def goto_home(request):
    activities = ActivityModel.objects.filter(user=request.user)
    logging.info("Fetched %d activities for user %s", len(activities), request.user)
    return render(
        request, "home.html", {"form": ActivityForm(), "activities": activities}
    )


def create_activity(request):
    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            logging.info("Succesfully created activity: %s", activity)
            return redirect("home")

    else:
        form = ActivityForm()

    return render(request, "home.html", {"form": form})


def delete_activity(request, activity_id):
    try:
        activity = ActivityModel.objects.get(id=activity_id, user=request.user)
        activity.delete()
        logging.info("Successfully deleted activity: %s", activity)
    except ActivityModel.DoesNotExist:
        logging.warning(
            "Attempted to delete non-existent activity with id: %s", activity_id
        )
    return redirect("home")
