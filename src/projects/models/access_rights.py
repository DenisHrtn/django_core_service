from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class AccessRights(AuditMixin, models.Model):
    """
    Модель для разрешений ролей
    """

    class TagsChoices(models.TextChoices):
        CREATOR = "creator", _("Создатель")
        EDITOR = "editor", _("Редактор")
        VIEWER = "viewer", _("Просмотр")
        DELETER = "deleter", _("Удаление")
        ADMIN = "admin", _("Администратор")

    access_right_id = models.BigAutoField(
        editable=False,
        primary_key=True,
        verbose_name=_("ID разрешения"),
    )

    access_right_name = models.CharField(
        unique=True,
        max_length=255,
        help_text=_("Имя разрешения для роли пользователя"),
        verbose_name=_("Название разрешения"),
    )

    description = models.CharField(
        max_length=255,
        help_text=_("Описание возможностей конкретного разрешения"),
        verbose_name=_("Описание"),
    )

    tag = models.CharField(
        max_length=12,
        choices=TagsChoices.choices,
        default=TagsChoices.VIEWER,
        verbose_name=_("Тип роли"),
        help_text=_("Категория разрешения: владелец, редактор, просмотр"),
    )
