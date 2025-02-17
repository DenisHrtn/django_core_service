import factory
from factory.django import DjangoModelFactory

from tickets.models import Ticket

from .project_factory import ProjectFactory


class TicketFactory(DjangoModelFactory):
    """
    Фабрика для генерации тестовых данных тикетов
    """

    class Meta:
        model = Ticket

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    status = factory.Faker(
        "random_element",
        elements=[choice[0] for choice in Ticket.StatusChoices.choices],
    )
    project = factory.SubFactory(ProjectFactory)
    creator = factory.Faker("email")
    assignee_ids = factory.List(
        [factory.Faker("random_int", min=1, max=100) for _ in range(3)]
    )
    ticket_notifications = factory.Faker("boolean")
    due_date = factory.Faker("date_time_this_year", before_now=False, after_now=True)
