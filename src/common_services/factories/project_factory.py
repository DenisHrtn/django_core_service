import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from projects.models import Project


class ProjectFactory(DjangoModelFactory):
    """
    Фабрика для генерации тестовых данных проектов
    """

    class Meta:
        model = Project

    name = factory.Faker("sentence", nb_words=2)
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.Faker("paragraph")

    @staticmethod
    @factory.post_generation
    def set_slug(obj, create, extracted, **kwargs):
        """
        Автоматически задаёт slug,
        если он не указан
        """
        if not obj.slug:
            obj.slug = slugify(obj.name)
            obj.save()
