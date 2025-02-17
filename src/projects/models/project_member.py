from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class ProjectMember(AuditMixin, models.Model):
    """
    Модель для участника проекта
    """

    member_id = models.BigAutoField(
        primary_key=True,
        unique=True,
        verbose_name=_("ID участника"),
    )

    project_id = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        help_text=_("Проект, который относится к конкретному участнику"),
        verbose_name=_("Проект"),
        db_index=True,
    )

    user_id = models.IntegerField(
        null=False,
        help_text=_("Пользователь, соотносящийся с участником"),
        verbose_name=_("ID пользователя"),
        db_index=True,
    )

    email = models.EmailField(
        max_length=255,
        null=False,
        help_text=_("Почта участника проекта"),
        verbose_name=_("Email"),
    )

    access_rights = ArrayField(
        models.IntegerField(),
        default=list,
        verbose_name=_("Разрешения"),
        help_text=_("Список разрешений участника"),
    )
