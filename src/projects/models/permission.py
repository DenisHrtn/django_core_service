import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Permission(models.Model):
    """
    Модель для разрешений ролей
    """

    class TagsChoices(models.TextChoices):
        OWNER = "owner", _("Владелец")
        EDITOR = "editor", _("Редактор")
        VIEWER = "viewer", _("Просмотр")

    permission_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name=_("ID разрешения"),
    )

    permission_name = models.CharField(
        unique=True,
        max_length=255,
        null=False,
        help_text=_("Имя разрешения для роли пользователя"),
        verbose_name=_("Название разрешения"),
    )

    description = models.CharField(
        max_length=255,
        null=False,
        help_text=_("Описание возможностей конкретного разрешения"),
        verbose_name=_("Описание"),
    )

    tag = models.CharField(
        max_length=6,
        choices=TagsChoices.choices,
        default=TagsChoices.VIEWER,
        null=False,
        verbose_name=_("Тип роли"),
        help_text=_("Категория разрешения: владелец, редактор, просмотр"),
    )
