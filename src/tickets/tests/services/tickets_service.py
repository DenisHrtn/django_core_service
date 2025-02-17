from unittest.mock import MagicMock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from common_services.factories import (
    ProjectFactory,
    ProjectMemberFactory,
    TicketFactory,
)
from common_services.utils.generate_jwt_token import generate_jwt_token
from tickets.models import Ticket
from tickets.services.ticket_service import TicketService


class TicketServiceTestCase(TestCase):
    """
    Тест-кейс для сервиса задач (тикетов)
    """

    def setUp(self):
        self.project = ProjectFactory()
        self.ticket = TicketFactory(project=self.project)

        self.user_id = 123
        self.admin_role = "admin"
        self.viewer_role = "viewer"

        self.project_member = ProjectMemberFactory(
            project_id=self.project, user_id=self.user_id, email="test@example.com"
        )

    def test_get_all_tickets(self):
        """
        Тест получения всех тикетов в проекте
        """
        with self.assertNumQueries(3):
            tickets = TicketService.get_all_tickets(self.project.project_id)
            self.assertEqual(
                tickets.count(), Ticket.objects.filter(project=self.project).count()
            )

    def test_get_ticket_by_id_success(self):
        """
        Тест получения тикета по ID
        """
        with self.assertNumQueries(2):
            ticket = TicketService.get_ticket_by_id(
                self.ticket.ticket_id, self.project.project_id
            )
            self.assertEqual(ticket, self.ticket)

    def test_get_ticket_by_id_not_found(self):
        """
        Тест получения несуществующего тикета (ожидаем исключение)
        """
        with self.assertRaises(ObjectDoesNotExist):
            TicketService.get_ticket_by_id(9999, self.project.project_id)

    def test_create_new_ticket_success(self):
        """
        Тест успешного создания тикета
        """
        token = generate_jwt_token(
            user_id=self.user_id, role_name=self.admin_role, email="test@example.com"
        )
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}

        data = {
            "title": "New Ticket",
            "description": "Test ticket description",
            "deadline": "2025-12-31T23:59:59Z",
        }

        with self.assertNumQueries(5):
            ticket = TicketService.create_new_ticket(
                project_id=self.project.project_id, data=data, request=request
            )

            self.assertEqual(ticket.title, data["title"])
            self.assertEqual(ticket.description, data["description"])
            self.assertEqual(ticket.creator, "test@example.com")

    def test_add_assignee_to_ticket_success(self):
        """
        Тест добавления исполнителя к тикету
        """
        with self.assertNumQueries(9):
            response = TicketService.add_assignee_to_ticket(
                project_id=self.project.project_id,
                ticket_id=self.ticket.ticket_id,
                user_id=self.user_id,
            )

            self.assertEqual(
                response["detail"],
                f"Юзер с ID {self.user_id} был успешно добавлен в задачу!",
            )

    def test_add_assignee_to_ticket_already_exists(self):
        """
        Тест повторного добавления участника в тикет
        """
        TicketService.add_assignee_to_ticket(
            project_id=self.project.project_id,
            ticket_id=self.ticket.ticket_id,
            user_id=self.user_id,
        )

        response = TicketService.add_assignee_to_ticket(
            project_id=self.project.project_id,
            ticket_id=self.ticket.ticket_id,
            user_id=self.user_id,
        )

        self.assertEqual(
            response["detail"], f"Юзер с ID {self.user_id} уже добавлен в задачу!"
        )

    def test_remove_assignee_from_ticket_success(self):
        """
        Тест успешного удаления участника из тикета
        """
        TicketService.add_assignee_to_ticket(
            project_id=self.project.project_id,
            ticket_id=self.ticket.ticket_id,
            user_id=self.user_id,
        )

        response = TicketService.remove_assignee_from_ticket(
            project_id=self.project.project_id,
            ticket_id=self.ticket.ticket_id,
            user_id=self.user_id,
        )

        self.assertEqual(
            response["detail"],
            f"Юзер с ID {self.user_id} был успешно удален из задачи!",
        )

    def test_remove_assignee_from_ticket_not_found(self):
        """
        Тест удаления участника, который не привязан к тикету
        """
        response = TicketService.remove_assignee_from_ticket(
            project_id=self.project.project_id,
            ticket_id=self.ticket.ticket_id,
            user_id=self.user_id,
        )

        self.assertEqual(
            response["detail"],
            f"Юзер с ID {self.user_id} не является участником задачи!",
        )
