from uuid import uuid4

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Task(models.Model):
    """
    Модель для задач
    """

    class StatusChoices(models.TextChoices):
        ARCHIVED = "ARCHIVED"
        TODO = "TODO"
        IN_PROGRESS = "IN_PROGRESS"
        COMPLETED = "COMPLETED"

    task_id = models.UUIDField(default=uuid4, editable=False, primary_key=True)

    title = models.CharField(
        max_length=255, null=False, unique=True, help_text="Название задачи"
    )

    description = models.TextField(null=True, help_text="Описание задачи")

    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.IN_PROGRESS,
        null=False,
        help_text="Статус задачи",
    )

    creator = models.CharField(
        max_length=255, null=False, help_text="Почта создателя конкретной задачи"
    )

    assignee_ids = ArrayField(
        models.IntegerField(),
        null=True,
        default=list,
        help_text="Список ID пользователей, назначенных на задачу",
    )

    task_notifications = models.BooleanField(
        default=True, null=False, help_text="Нужны ли уведомления по таске"
    )

    due_date = models.DateTimeField(
        null=True, blank=True, help_text="Дедлайн выполнения задачи"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
