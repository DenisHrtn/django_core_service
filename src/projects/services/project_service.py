from typing import Dict, List, Optional, Union

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import transaction
from django.http import HttpRequest
from rest_framework.exceptions import NotFound

from common_services.permissions.check_permissions import PermissionCheck
from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models.project import Project
from projects.models.project_member import ProjectMember
from projects.models.role import Role
from projects.serializers.project_serializer import ProjectSerializer


class ProjectService:
    """
    Сервис для CRUD-операций и
    различных методов над сущностями Project
    """

    @staticmethod
    def get_all_projects(request: HttpRequest) -> List[Project]:
        """
        Метод для получения всех доступных проектов
        :param token: JWT-token
        :return: project(-s) if any
        """
        user_id, role_name, _ = decode_jwt_token(request)

        if role_name == "admin":
            return Project.objects.all()

        projects = (
            Project.objects.prefetch_related("projectmember_set")
            .filter(projectmember__user_id=user_id)
            .distinct()
        )
        return projects

    @staticmethod
    def get_project_by_id(project_id: str, request: HttpRequest) -> Optional[Project]:
        """
        Метод для получения конкретного проекта
        :param project_id: project id
        :param token: JWT-token
        :return: project if any
        """
        user_id, role_name, _ = decode_jwt_token(request)

        if role_name == "admin":
            try:
                project = Project.objects.get(pk=project_id)
                return project
            except ObjectDoesNotExist as exc:
                raise NotFound("Проект не найден") from exc
        else:
            try:
                project = Project.objects.prefetch_related("projectmember_set").get(
                    project_id=project_id, projectmember__user_id=user_id
                )
                return project
            except ObjectDoesNotExist as exc:
                raise NotFound("Проект не найден") from exc

    @staticmethod
    def create_new_project(
        data: Dict[str, Union[str, int]],
        request: HttpRequest,
    ) -> Dict[str, Union[str, int]]:
        """
        Метод для создания проекта
        :param data: request data
        :param token: JWT-token
        :return: new project
        """
        user_id, role_name, email = decode_jwt_token(request)
        print(user_id, role_name, email)
        permission_check = PermissionCheck(role_name=role_name)

        if not permission_check.can_create():
            raise PermissionDenied("Вы не можете создавать проекты!")

        role_permissions = (
            Role.objects.filter(role_name=role_name)
            .values_list("permissions", flat=True)
            .first()
        )

        with transaction.atomic():
            serializer = ProjectSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                project = serializer.save()

                project_member = ProjectMember.objects.create(
                    project_id=project,
                    user_id=user_id,
                    email=email,
                    permissions=role_permissions,
                )
                project_member.save()

                return serializer.data
            return serializer.errors

    @staticmethod
    def update_project(
        data: Dict[str, Union[str, int]], request: HttpRequest
    ) -> Dict[str, Union[str, int]]:
        """
        Метод для обновления проекта
        :param data: request data
        :param token: JWT-token
        :return: data
        """
        _, role_name, _ = decode_jwt_token(request)

        permission_check = PermissionCheck(role_name=role_name)

        if not permission_check.can_update():
            raise PermissionDenied("Вы не можете обновлять проект!")

        project_id = data.get("project_id") or request.parser_context["kwargs"].get(
            "pk"
        )

        if not project_id:
            raise ObjectDoesNotExist("Не указан project_id")

        try:
            project = Project.objects.get(project_id=project_id)
        except ObjectDoesNotExist as exc:
            raise NotFound("Проект не найден") from exc

        serializer = ProjectSerializer(instance=project, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data
        return serializer.errors

    @staticmethod
    def delete_project(request: HttpRequest, project_id: int) -> Dict[str, str]:
        """
        Метод для удаления проекта
        :param data: request data
        :param token: JWT-token
        :param project_id: project id
        :return:
        """
        _, role_name, _ = decode_jwt_token(request)

        permission_check = PermissionCheck(role_name=role_name)

        if not permission_check.can_delete():
            raise PermissionDenied("Вы не можете удалять проекты!")

        with transaction.atomic():
            try:
                project = Project.objects.get(project_id=project_id)
            except ObjectDoesNotExist as exc:
                raise NotFound("Проект не найден") from exc

            project.delete()

            return {"detail": "Проект успешно удален"}
