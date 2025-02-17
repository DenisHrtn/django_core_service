import random

import factory
from factory.django import DjangoModelFactory

from common_services.factories.project_factory import ProjectFactory
from projects.models import ProjectMember


class ProjectMemberFactory(DjangoModelFactory):
    """
    Фабрика для генерации тестовых данных участника проекта
    """

    class Meta:
        model = ProjectMember

    project_id = factory.SubFactory(ProjectFactory)
    user_id = factory.Sequence(lambda n: n + 1)
    email = factory.Faker("email")
    access_rights = factory.LazyFunction(
        lambda: [random.randint(1, 5) for _ in range(3)]
    )
