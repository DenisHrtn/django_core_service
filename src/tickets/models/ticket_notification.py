from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class TicketNotification(AuditMixin, models.Model):
    """
    Модель уведомления для задачи
    """

    notification_id = models.BigAutoField(
        editable=False,
        primary_key=True,
        verbose_name=_("ID уведомления"),
    )

    ticket = models.ForeignKey(
        "tickets.Ticket",
        on_delete=models.CASCADE,
        null=False,
        help_text=_("Задача, к которой привязано уведомление"),
        verbose_name=_("Задача"),
    )

    user_id = models.IntegerField(
        null=False,
        help_text=_("Пользователь, которому отправится уведомление"),
        verbose_name=_("Пользователь"),
    )

    notify_time = models.DateTimeField(
        help_text=_("Время отправки уведомления"),
        verbose_name=_("Время уведомления"),
    )
