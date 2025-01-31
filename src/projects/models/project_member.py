import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


class ProjectMember(models.Model):
    """
    Модель для участника проекта
    """

    member_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project_id = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        null=False,
        help_text="Проект, который относится к конкретному участнику",
    )

    user_id = models.IntegerField(
        null=False, help_text="Пользователь соотносящийся с участником"
    )

    email = models.EmailField(
        max_length=255, null=False, help_text="Почта участника проекта"
    )

    permissions = ArrayField(models.IntegerField(), default=list)
