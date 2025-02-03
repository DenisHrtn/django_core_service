import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    """
    Модель роли с ее пермишшенами
    """

    role_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        help_text=_("ID роли"),
        verbose_name=_("ID"),
    )

    role_name = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        help_text=_("Название роли"),
        verbose_name=_("Название"),
    )

    description = models.TextField(
        null=False, help_text=_("Описание роли"), verbose_name=_("Описание")
    )

    permissions = ArrayField(
        models.IntegerField(),
        null=True,
        help_text=_("Разрешения для роли"),
        verbose_name=_("Разршения"),
    )

    user_id = models.IntegerField(
        null=False,
        help_text=_("Пользователь, соотносящийся с ролью"),
        verbose_name=_("ID пользователя"),
    )
