import random

import factory
from factory.django import DjangoModelFactory

from projects.models import Role


class RoleFactory(DjangoModelFactory):
    """
    Фабрика для генерации тестовых данных модели Role
    """

    class Meta:
        model = Role

    role_name = factory.Faker("job")
    description = factory.Faker("sentence")
    access_rights = factory.LazyFunction(
        lambda: [random.randint(1, 5) for _ in range(2)]
    )
    user_id = factory.Sequence(lambda n: n + 1)
