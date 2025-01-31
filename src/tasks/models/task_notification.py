from uuid import uuid4

from django.db import models


class TaskNotification(models.Model):
    """
    Модель уведомления для задачи
    """

    notification_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    task_id = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        null=False,
        help_text="Задача к которой крепится уведомление",
    )

    user_id = models.IntegerField(
        null=False, help_text="Пользователь, которому отправится уведомление"
    )
    notify_time = models.DateTimeField(help_text="Время отправки уведомления")
