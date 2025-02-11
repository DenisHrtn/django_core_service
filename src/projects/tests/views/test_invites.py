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

    def test_send_invite(self):
        """
        Проверка отправки инвайта  TODO: допилить мок для селери
        """
        url = reverse(
            "project-invites-create", kwargs={"project_id": self.project1.project_id}
        )
        data = {"email": "denis@gmail.com"}
        response = self.client.post(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_invite(self):
        """
        Проверка принятия инвайта  TODO: also some fixes
        """
        url = reverse(
            "project-invites-accept", kwargs={"project_id": self.project1.project_id}
        )
        data = {"token": self.invite.token, "invite_response": True}
        response = self.client.patch(
            url, data, HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
