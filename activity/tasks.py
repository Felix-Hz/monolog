from celery import shared_task


@shared_task
def dummy_task():
    print("This is a dummy task.")
