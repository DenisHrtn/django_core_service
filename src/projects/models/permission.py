import uuid

from django.db import models


class Permission(models.Model):
    """
    Модель для разрешений ролей
    """

    class TagsChoices(models.TextChoices):
        OWNER = "owner"
        EDITOR = "editor"
        VIEWER = "viewer"

    permission_id = models.UUIDField(
        default=uuid.uuid4, editable=False, primary_key=True
    )

    permission_name = models.CharField(
        unique=True,
        max_length=255,
        null=False,
        help_text="Имя разрешения для роли пользователя",
    )

    description = models.CharField(
        max_length=255,
        null=False,
        help_text="Описание возможностей конкретного разрешения",
    )

    tag = models.CharField(
        max_length=6,
        choices=TagsChoices.choices,
        default=TagsChoices.VIEWER,
        null=False,
    )
