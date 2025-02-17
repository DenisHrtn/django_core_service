from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from common_services.factories import ProjectFactory, ProjectMemberFactory, RoleFactory
from projects.models import ProjectMember
from projects.services.project_members_service import ProjectMembersService


class ProjectMembersServiceTestCase(TestCase):
    """
    Тест-кейс для сервиса работы с участниками проекта
    """

    def setUp(self):
        self.project1 = ProjectFactory()
        self.project2 = ProjectFactory()

        self.user_id = 123
        self.admin_role = RoleFactory(role_name="admin", user_id=self.user_id)
        self.viewer_role = RoleFactory(role_name="viewer", user_id=self.user_id)
        self.deleter_role = RoleFactory(role_name="deleter", user_id=self.user_id)

        self.project_member = ProjectMemberFactory(
            project_id=self.project1, user_id=self.user_id, access_rights=[1, 2]
        )

    def test_get_all_project_members_by_viewer(self):
        """
        Обычный пользователь видит только участников своего проекта,
        в которых он состоит, а админ - всех.
        """
        with self.assertNumQueries(3):
            project_members = ProjectMembersService.get_project_members(
                project_id=self.project1.project_id,
                role_name=self.viewer_role.role_name,
            )
            self.assertEqual(project_members.count(), 1)
            self.assertEqual(project_members.first(), self.project_member)

    def test_get_all_project_members_by_admin(self):
        """
        Админ должен видеть всех участников проекта.
        """
        with self.assertNumQueries(3):
            project_members = ProjectMembersService.get_project_members(
                project_id=self.project1.project_id, role_name=self.admin_role.role_name
            )
            self.assertEqual(project_members.count(), 1)
            self.assertEqual(project_members.first(), self.project_member)

    def test_get_project_by_id_exists(self):
        """
        Тест получения участника проекта
        по ID (существующему)
        """
        with self.assertNumQueries(1):
            project_member = ProjectMembersService.get_project_member_by_id(
                self.project1.project_id, self.project_member.member_id
            )
            self.assertEqual(project_member, self.project_member)

    def test_delete_project_member_by_admin(self):
        """
        Тест успешного удаления проекта
        """
        with self.assertNumQueries(3):
            ProjectMembersService.delete_project_member(
                project_id=self.project1.project_id,
                member_id=self.project_member.member_id,
            )

            with self.assertRaises(ObjectDoesNotExist):
                ProjectMember.objects.get(
                    pk=self.project_member.member_id,
                    project_id=self.project1.project_id,
                )
