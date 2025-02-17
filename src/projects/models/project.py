from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from common_services.mixins.audit_model_mixin import AuditMixin


class Project(AuditMixin, models.Model):
    """
    Модель для таблицы проектов
    """

    project_id = models.BigAutoField(
        primary_key=True,
        editable=False,
        verbose_name=_("ID проекта"),
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        help_text=_("Имя проекта"),
        verbose_name=_("Название"),
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        help_text=_("Читаемый URL проекта"),
        verbose_name=_("Slug"),
    )

    description = models.TextField(
        null=True,
        help_text=_("Описание проекта"),
        verbose_name=_("Описание"),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            original_slug = self.slug
            counter = 1
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
