from unittest.mock import patch
from uuid import UUID

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common_services.factories import InviteFactory, ProjectFactory
from common_services.utils.generate_jwt_token import generate_jwt_token


class InvitesTestCase(APITestCase):
    """
    Тест-кейс для тестирования ручек инвайтов
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.project1 = ProjectFactory()

        self.user_id = 1
        self.email = "denis@gmail.com"

        self.invite = InviteFactory(project=self.project1, email=self.email)

        self.token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )

    def test_get_invites_list(self):
        """
        Получения всех инвайтов
        """
        url = reverse("project-invites-list", kwargs={"project_id": 1})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invites_detail(self):
        """
        Получение конкретного инвайта
        """
        url = reverse(
            "project-invites-detail",
            kwargs={
                "project_id": self.project1.project_id,
                "invite_id": self.invite.invite_id,
            },
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("projects.tasks.send_invite_token_to_email.delay")
    @patch(
        "projects.services.project_invite_service."
        "ProjectInviteService.generate_invite_token",
        return_value=UUID("7d69e55f-45b7-4606-aa40-f80c3bd28c04"),
    )
    def test_send_invite(self, mock_generate_token, mock_task):
        """
        Проверка отправки инвайта
        """
        url = reverse(
            "project-invites-create", kwargs={"project_id": self.project1.project_id}
        )
        data = {"email": "denis23@gmail.com"}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_task.assert_called_once_with(
            to_address="denis23@gmail.com",
            token="7d69e55f-45b7-4606-aa40-f80c3bd28c04",
            project_name=self.project1.name,
        )
