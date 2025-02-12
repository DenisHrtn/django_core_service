from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from projects.models import ProjectMember


class ProjectMembersService:
    """
    Сервис для CRUD-операций с участниками проекта
    """

    @staticmethod
    def is_project_member(project_id: int, user_id: int) -> bool:
        return ProjectMember.objects.filter(
            project_id=project_id, user_id=user_id
        ).exists()

    @staticmethod
    def get_project_members(project_id: int, role_name: str) -> List[ProjectMember]:
        """
        Метод для получения всех участников проекта
        :param project_id: int
        :param role_name: str
        :return: list of project members
        """
        project_members = ProjectMember.objects.filter(project_id=project_id)

        if not project_members.exists():
            raise NotFound("Проект не найден")

        if role_name == "admin":
            return project_members.select_related("project_id")

        return project_members

    @staticmethod
    def get_project_member_by_id(
        project_id: int, member_id: int
    ) -> Optional[ProjectMember]:
        """
        Метод для получения конкретного участника проекта
        :param project_id: int
        :param member_id: int
        :return: project member if any
        """
        try:
            return ProjectMember.objects.filter(
                project_id=project_id, member_id=member_id
            ).first()
        except ObjectDoesNotExist as exc:
            raise NotFound("Участник проекта не найден") from exc

    @staticmethod
    def delete_project_member(member_id: int, project_id: int):
        """
        Метод для удаления участника с проекта
        :param member_id: int
        :param project_id: int
        :return: None
        """
        try:
            member = ProjectMember.objects.filter(
                member_id=member_id, project_id=project_id
            ).first()
            if member:
                member.delete()
                return {"detail": "Участник успешно удален с проекта"}
        except ObjectDoesNotExist as exc:
            raise ObjectDoesNotExist("Проект не найден") from exc
