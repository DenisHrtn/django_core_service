import uuid

import factory
from django.utils.timezone import now
from factory.django import DjangoModelFactory

from common_services.factories import ProjectFactory
from projects.models import Invite


class InviteFactory(DjangoModelFactory):
    """
    Фабрика для генерации тестовых данных инвайтов
    """

    class Meta:
        model = Invite

    project = factory.SubFactory(ProjectFactory)
    token = factory.LazyFunction(uuid.uuid4)
    email = factory.Faker("email")
    status = Invite.StatusChoices.PENDING
    created_at = factory.LazyFunction(now)
