from typing import Dict, List, Optional, Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpRequest
from rest_framework.exceptions import NotFound

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models import Project, ProjectMember, Role
from projects.serializers.project_serializer import ProjectSerializer


class ProjectService:
    """
    Сервис для CRUD-операций с проектами.
    """

    @staticmethod
    def get_all_projects(user_id: int, role_name: str) -> List[Project]:
        """
        Получение всех проектов
        :param user_id: int
        :param role_name: str
        :return: list of projects
        """
        if role_name == "admin":
            return Project.objects.all()

        return (
            Project.objects.prefetch_related("projectmember_set")
            .filter(projectmember__user_id=user_id)
            .distinct()
        )

    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Project]:
        """
        Получение конкретного проекта
        :param project_id: int
        :return: project if any
        """
        try:
            return Project.objects.get(pk=project_id)
        except ObjectDoesNotExist as exc:
            raise NotFound("Проект не найден") from exc

    @staticmethod
    def create_new_project(
        data: Dict[str, Union[str, int]], request: HttpRequest
    ) -> Dict[str, Union[str, int]]:
        """
        Создание проекта
        :param data: dict
        :param request: HttpRequest
        :return: new project
        """
        user_id, role_name, email = decode_jwt_token(request=request)

        role_permissions = (
            Role.objects.filter(role_name=role_name)
            .values_list("permissions", flat=True)
            .first()
        )

        with transaction.atomic():
            serializer = ProjectSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            project = serializer.save()

            ProjectMember.objects.create(
                project_id=project,
                user_id=user_id,
                email=email,
                permissions=role_permissions,
            )

            return {"id": project.project_id, **serializer.data}

    @staticmethod
    def update_project(data, project: Project) -> Project:
        """
        Обновление проекта
        :param data: dict
        :param project: Project
        :return: updated project
        """
        serializer = ProjectSerializer(instance=project, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete_project(project: Project):
        """
        Удаление проекта
        :param project:
        :return: message about successfully deleted project
        """
        if Project.objects.filter(pk=project.pk).exists():
            project.delete()
            return {"detail": "Проект успешно удален"}
        raise ObjectDoesNotExist("Проект не найден")
