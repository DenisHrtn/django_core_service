import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class Invite(AuditMixin, models.Model):
    """
    Модель для инвайтов в проект пользователей
    """

    class StatusChoices(models.TextChoices):
        PENDING = "pending", _("Ожидает подтверждения")
        ACCEPTED = "accepted", _("Принято")
        REJECTED = "rejected", _("Отклонено")

    invite_id = models.BigAutoField(
        primary_key=True,
        editable=False,
        verbose_name=_("ID инвайта"),
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="invites",
        help_text=_("Проект"),
        verbose_name=_("Проект"),
        db_index=True,
    )

    token = models.CharField(
        max_length=36,
        default=uuid.uuid4,
        unique=True,
        help_text=_("Специальный токен"),
        verbose_name=_("Токен инвайта"),
    )

    email = models.EmailField(
        null=False,
        help_text=_("Почта пользователя"),
        verbose_name=_("Email приглашенного"),
    )

    status = models.CharField(
        max_length=8,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name=_("Статус инвайта"),
        help_text=_("Статус приглашения: ожидает, принято, отклонено"),
    )
