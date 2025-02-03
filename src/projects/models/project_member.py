import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class ProjectMember(models.Model):
    """
    Модель для участника проекта
    """

    member_id = models.SlugField(
        primary_key=True,
        max_length=36,
        unique=True,
        default=lambda: str(uuid.uuid4()),
        verbose_name=_("ID участника"),
    )

    project_id = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        help_text=_("Проект, который относится к конкретному участнику"),
        verbose_name=_("Проект"),
    )

    user_id = models.IntegerField(
        null=False,
        help_text=_("Пользователь, соотносящийся с участником"),
        verbose_name=_("ID пользователя"),
    )

    email = models.EmailField(
        max_length=255,
        null=False,
        help_text=_("Почта участника проекта"),
        verbose_name=_("Email"),
    )

    permissions = ArrayField(
        models.IntegerField(),
        default=list,
        verbose_name=_("Разрешения"),
        help_text=_("Список разрешений участника"),
    )
