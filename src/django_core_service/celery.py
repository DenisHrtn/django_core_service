import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_core_service.settings")

app = Celery("django_core_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Prints the request information for debugging purposes.

    :param self: The current task instance.
    """
    print(f"Request: {self.request!r}")
