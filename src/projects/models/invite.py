import uuid

from django.db import models


class Invite(models.Model):
    """
    Модель для инвайтов в проект пользователей
    """

    class StatusChoices(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        REJECTED = "rejected"

    invite_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    project_id = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="invites",
        help_text="Проект к которому был сделан инвайт для пользователя",
    )

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        help_text="Специальный токен отправляемый на почту приглашенному пользователю",
    )

    email = models.EmailField(
        null=False,
        help_text="Почта пользователя на которую придет приглашение на проект",
    )

    status = models.CharField(
        max_length=8, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
