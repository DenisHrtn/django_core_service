from django.test import TestCase

from common_services.factories import (
    InviteFactory,
    ProjectFactory,
    ProjectMemberFactory,
    RoleFactory,
)
from projects.services.project_invite_service import ProjectInviteService


class ProjectInviteServiceTestCase(TestCase):
    """
    Тест-кейс для сервиса работы с инвайтами
    """

    def setUp(self):
        self.project1 = ProjectFactory()

        self.user_id = 123
        self.admin_role = RoleFactory(role_name="admin", user_id=self.user_id)
        self.editor_role = RoleFactory(role_name="editor", user_id=self.user_id)
        self.viewer_role = RoleFactory(role_name="viewer", user_id=self.user_id)

        self.project_member = ProjectMemberFactory(
            project_id=self.project1, user_id=self.user_id, access_rights=[1, 2]
        )

        self.invite = InviteFactory(project=self.project1)

    def test_get_all_invites_by_admin(self):
        """
        Просмотр всех инвайтов по конкретному проекту
        через роль администратора
        """
        with self.assertNumQueries(2):
            invites = ProjectInviteService.get_all_invites(
                self.user_id, self.project1.project_id, self.admin_role
            )
            self.assertEqual(invites.count(), 1)
            self.assertEqual(invites.first(), self.invite)

    def test_get_all_invites_by_editor(self):
        """
        Просмотр всех инвайтов по конкретному проекту
        через роль редактора проекта
        """
        with self.assertNumQueries(2):
            invites = ProjectInviteService.get_all_invites(
                self.user_id, self.project1.project_id, self.editor_role
            )
            self.assertEqual(invites.count(), 1)
            self.assertEqual(invites.first(), self.invite)

    def test_get_invite_by_id(self):
        """
        Просмотр конкретного инвайта
        """
        with self.assertNumQueries(1):
            invite = ProjectInviteService.get_invite_by_id(self.invite.invite_id)
            self.assertEqual(invite, self.invite)
