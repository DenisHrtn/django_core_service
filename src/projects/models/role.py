from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class Role(AuditMixin, models.Model):
    """
    Модель роли с ее пермишшенами
    """

    role_id = models.BigAutoField(
        editable=False,
        primary_key=True,
        help_text=_("ID роли"),
        verbose_name=_("ID"),
    )

    role_name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Название роли"),
        verbose_name=_("Название"),
    )

    description = models.TextField(
        null=False, help_text=_("Описание роли"), verbose_name=_("Описание")
    )

    access_rights = ArrayField(
        models.IntegerField(),
        null=True,
        help_text=_("Разрешения для роли"),
        verbose_name=_("Разршения"),
    )

    user_id = models.IntegerField(
        help_text=_("Пользователь, соотносящийся с ролью"),
        verbose_name=_("ID пользователя"),
    )
