from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common_services.factories.project_factory import ProjectFactory
from common_services.factories.project_member_factory import ProjectMemberFactory
from common_services.utils.generate_jwt_token import generate_jwt_token


class ProjectMembersTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.project1 = ProjectFactory()
        self.project2 = ProjectFactory()

        self.user_id = 123

        self.project_member = ProjectMemberFactory(
            project_id=self.project1, user_id=self.user_id, access_rights=[1, 2]
        )

        self.token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )

        self.data = {"access_rights": [1, 2, 3]}

    def test_project_member_list(self):
        """
        Тест для проверки получения всех мемберов проекта
        """
        url = reverse(
            "project-members-list",
            kwargs={"project_id": self.project1.project_id},
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_member_detail(self):
        """
        Тест для проверки получения конкретного мембера
        """
        url = reverse(
            "project-members-detail",
            kwargs={
                "project_id": self.project1.project_id,
                "member_id": self.project_member.member_id,
            },
        )
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_member_partial_update(self):
        """
        Тест для проверки частичного обновления мембера
        """
        url = reverse(
            "project-members-update",
            kwargs={
                "project_id": self.project1.project_id,
                "member_id": self.project_member.member_id,
            },
        )
        response = self.client.patch(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_member_delete(self):
        """
        Тест для проверки удаления мембера проекта
        """
        url = reverse(
            "project-members-delete",
            kwargs={
                "project_id": self.project1.project_id,
                "member_id": self.project_member.member_id,
            },
        )
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
