from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from common_services.factories.project_factory import ProjectFactory
from common_services.factories.project_member_factory import ProjectMemberFactory
from common_services.utils.generate_jwt_token import generate_jwt_token


class ProjectViewsTestCase(APITestCase):
    """
    Тест-кейс для тестирования ручек проектов
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.project1 = ProjectFactory()
        self.project2 = ProjectFactory()

        self.user_id = 1

        self.project_member = ProjectMemberFactory(
            project_id=self.project1, user_id=self.user_id, access_rights=[1]
        )

        self.token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )

        self.data = {
            "name": "New Test Project",
            "description": "A test project",
        }

    def test_get_project_list(self):
        """
        Тест для получения всех проектов
        """
        url = reverse("projects-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_detail(self):
        """
        Тест для получения конкретного проекта
        """
        url = reverse("projects-detail", kwargs={"pk": self.project1.pk})
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project(self):
        """
        Тест для провеки создания проекта
        """
        url = reverse("project-create")
        response = self.client.post(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}", data=self.data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_project(self):
        """
        Тест для проверки обновления проектов
        """
        url = reverse(
            "project-update",
            kwargs={"pk": self.project1.pk},
        )
        response = self.client.put(
            url, HTTP_AUTHORIZATION=f"Bearer {self.token}", data=self.data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        """
        Тест для проверки удаления проекта
        """
        url = reverse("project-delete", kwargs={"pk": self.project1.pk})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_all_projects_with_tasks(self):
        """
        Тест для проверки получения проектов с их задачами
        """
        url = reverse("projects-tasks-list")
        response = self.client.get(url, HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
