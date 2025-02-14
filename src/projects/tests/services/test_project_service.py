from unittest.mock import MagicMock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework.exceptions import NotFound, ValidationError

from common_services.factories import ProjectFactory, ProjectMemberFactory, RoleFactory
from common_services.utils.generate_jwt_token import generate_jwt_token
from projects.models import Project, ProjectMember
from projects.services.project_service import ProjectService


class ProjectServiceTestCase(TestCase):
    """
    Тест-кейс для сервиса проектов
    """

    def setUp(self):
        self.project1 = ProjectFactory()
        self.project2 = ProjectFactory()

        self.user_id = 123
        self.admin_role = RoleFactory(role_name="admin", user_id=self.user_id)
        self.viewer_role = RoleFactory(role_name="viewer", user_id=self.user_id)

        self.project_member = ProjectMemberFactory(
            project_id=self.project1, user_id=self.user_id, access_rights=[1, 2]
        )

    def test_get_all_projects_admin(self):
        """
        Администратор должен получать все проекты
        """
        with self.assertNumQueries(2):
            projects = ProjectService.get_all_projects(
                user_id=self.user_id, role_name="admin"
            )
            self.assertEqual(projects.count(), Project.objects.count())

    def test_get_all_projects_viewer(self):
        """
        Обычный пользователь видит только те проекты,
        в которых он состоит.
        """
        with self.assertNumQueries(3):
            projects = ProjectService.get_all_projects(
                user_id=self.user_id, role_name="viewer"
            )
            self.assertEqual(projects.count(), 1)
            self.assertEqual(projects.first(), self.project1)

    def test_get_project_by_id_exists(self):
        """
        Тест получения проекта
        по ID (существующего).
        """
        with self.assertNumQueries(1):
            project = ProjectService.get_project_by_id(self.project1.project_id)
            self.assertEqual(project, self.project1)

    def test_get_project_by_id_not_found(self):
        """
        Тест получения проекта по несуществующему ID
        (должен вызвать исключение).
        """
        with self.assertNumQueries(1):
            with self.assertRaises(NotFound):
                ProjectService.get_project_by_id(9999)

    def test_create_project_success(self):
        """
        Тест успешного создания проекта
        """
        token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}

        data = {
            "name": "New Test Project",
            "description": "A test project",
        }

        with self.assertNumQueries(8):
            project = ProjectService.create_new_project(data=data, request=request)

            self.assertEqual(project["name"], data["name"])
            self.assertEqual(project["description"], data["description"])
            self.assertTrue(
                ProjectMember.objects.filter(
                    project_id=project["id"], user_id=self.user_id
                ).exists()
            )

    def test_create_project_invalid_data(self):
        """
        Тест создания проекта с невалидными данными
        (должен вызывать исключение)
        """
        token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}

        data = {
            "name": "",
            "description": "A test project",
        }

        with self.assertRaises(ValidationError):
            ProjectService.create_new_project(data=data, request=request)

    def test_delete_project_success(self):
        """
        Тест успешного удаления проекта
        """
        project_id = self.project1.project_id

        with self.assertNumQueries(6):
            ProjectService.delete_project(self.project1)

            with self.assertRaises(ObjectDoesNotExist):
                Project.objects.get(project_id=project_id)

    def test_delete_project_nonexistent(self):
        """
        Тест удаления несуществующего проекта (ожидаем ошибку)
        """
        fake_project = Project(project_id=9999)
        with self.assertRaises(ObjectDoesNotExist):
            ProjectService.delete_project(fake_project)

    def test_get_projects_with_tasks(self):
        """
        Тест получения всех проектов с тасками
        """
        token = generate_jwt_token(
            user_id=self.user_id, role_name="admin", email="test@example.com"
        )
        request = MagicMock()
        request.headers = {"Authorization": f"Bearer {token}"}

        with self.assertNumQueries(1):
            projects_tasks = ProjectService.get_all_projects_with_tasks(request=request)

            self.assertEqual(projects_tasks.count(), 2)
