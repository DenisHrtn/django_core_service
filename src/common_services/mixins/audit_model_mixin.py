from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditMixin(models.Model):
    """
    Миксин для отслеживания изменений в модели
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата создания"),
        help_text=_("Дата и время создания задачи"),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Дата обновления"),
        help_text=_("Дата и время последнего обновления задачи"),
    )

    class Meta:
        abstract = True
