from django.db import models


class AuditMixin(models.Model):
    """
    Миксин для отслеживания изменений в модели
    """

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
