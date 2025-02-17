from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class Ticket(AuditMixin, models.Model):
    """
    Модель для задач
    """

    class StatusChoices(models.TextChoices):
        ARCHIVED = "ARCHIVED", _("Архивировано")
        TODO = "TODO", _("К выполнению")
        IN_PROGRESS = "IN_PROGRESS", _("В процессе")
        COMPLETED = "COMPLETED", _("Завершено")

    ticket_id = models.BigAutoField(
        editable=False,
        primary_key=True,
        verbose_name=_("ID задачи"),
    )

    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text=_("Название задачи"),
        verbose_name=_("Заголовок"),
    )

    description = models.TextField(
        null=True,
        help_text=_("Описание задачи"),
        verbose_name=_("Описание"),
    )

    status = models.CharField(
        max_length=15,
        choices=StatusChoices.choices,
        default=StatusChoices.TODO,
        help_text=_("Статус задачи"),
        verbose_name=_("Статус"),
        db_index=True,
    )

    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.PROTECT,
        related_name="tickets",
        help_text=_("Проект"),
        verbose_name=_("Проект"),
        db_index=True,
    )

    creator = models.EmailField(
        max_length=255,
        help_text=_("Почта создателя конкретной задачи"),
        verbose_name=_("Создатель"),
    )

    assignee_ids = ArrayField(
        models.IntegerField(),
        null=True,
        default=list,
        help_text=_("Список ID пользователей, назначенных на задачу"),
        verbose_name=_("Назначенные пользователи"),
    )

    ticket_notifications = models.BooleanField(
        default=False,
        help_text=_("Нужны ли уведомления по задаче"),
        verbose_name=_("Уведомления"),
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Дедлайн выполнения задачи"),
        verbose_name=_("Крайний срок"),
        db_index=True,
    )
