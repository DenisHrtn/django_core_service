import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Project(models.Model):
    """
    Модель для таблицы проектов
    """

    project_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID проекта"),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        help_text=_("Имя проекта"),
        verbose_name=_("Название"),
    )

    description = models.TextField(
        null=True,
        help_text=_("Описание проекта"),
        verbose_name=_("Описание"),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания"),
        help_text=_("Дата и время создания проекта"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления"),
        help_text=_("Дата и время последнего обновления проекта"),
    )
