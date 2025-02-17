import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_core_service.settings")

app = Celery("django_core_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-ticket-notifications-every-minute": {
        "task": "tickets.tasks.send_ticket_notification",
        "schedule": crontab(minute="*/1"),
    },
}


@app.task(bind=True)
def debug_task(self):
    """
    Prints the request information for debugging purposes.

    :param self: The current task instance.
    """
    print(f"Request: {self.request!r}")
