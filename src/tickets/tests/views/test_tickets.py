from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common_services.factories import ProjectFactory, TicketFactory
from common_services.utils.generate_jwt_token import generate_jwt_token


class TicketTestCase(APITestCase):
    """
    Тест-кейс для тестирования ручек тикетов
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.project = ProjectFactory()
        self.user_id = 1
        self.email = "denis@gmail.com"

        self.ticket = TicketFactory(project=self.project, creator=self.email)

        self.token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@gmail.com"
        )

    def test_get_tickets_list(self):
        """
        Получение списка всех тикетов
        """
        url = reverse("tickets-list", kwargs={"project_id": self.project.project_id})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ticket_detail(self):
        """
        Получение конкретного тикета
        """
        url = reverse(
            "tickets-detail",
            kwargs={
                "project_id": self.project.project_id,
                "ticket_id": self.ticket.ticket_id,
            },
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ticket(self):
        """
        Проверка создания тикета
        """
        url = reverse("tickets-create", kwargs={"project_id": self.project.project_id})
        data = {
            "title": "Новая задача",
            "description": "Описание новой задачи",
            "status": "TODO",
            "creator": "test@gmail.com",
            "assignee_ids": [2, 3],
            "ticket_notifications": False,
            "due_date": "2025-02-20T12:00:00Z",
        }
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_ticket(self):
        """
        Проверка обновления тикета
        """
        url = reverse(
            "tickets-update",
            kwargs={
                "project_id": self.project.project_id,
                "ticket_id": self.ticket.ticket_id,
            },
        )
        data = {"title": "Обновленный заголовок", "status": "IN_PROGRESS"}
        response = self.client.patch(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ticket(self):
        """
        Проверка удаления тикета
        """
        url = reverse(
            "tickets-delete",
            kwargs={
                "project_id": self.project.project_id,
                "ticket_id": self.ticket.ticket_id,
            },
        )
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
