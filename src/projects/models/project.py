import uuid

from django.db import models


class Project(models.Model):
    """
    Модель для таблицы проектов
    """

    project_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        max_length=255, unique=True, null=False, help_text="Имя проекта"
    )

    description = models.TextField(null=True, help_text="Описание проекта")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
