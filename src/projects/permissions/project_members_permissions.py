from rest_framework.permissions import BasePermission

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models import ProjectMember, Role


class ProjectMemberPermissions(BasePermission):
    """
    Кастомный пермишен для проверки
    прав доступа к участникам проекта
    """

    def has_permission(self, request, view):
        """
        Проверка доступа на уровне запроса
        """
        user_id, role_name, _ = decode_jwt_token(request)
        request.user_id = user_id
        request.role_name = role_name

        project_member = (
            ProjectMember.objects.select_related("project_id")
            .filter(user_id=user_id)
            .first()
        )

        request.project_id = project_member.project_id.project_id

        if role_name == "admin":
            return True

        match view.action:
            case "update":
                return self._can_update(role_name)
            case "delete":
                return self._can_delete(role_name)

        return True

    def has_object_permission(self, request, view, obj):
        """
        Проверка на уровне доступа объекта
        """
        user_id = request.user_id
        role_name = request.role_name

        if role_name == "admin":
            return True

        is_member = ProjectMember.objects.filter(
            project_id=obj.project_id, user_id=user_id
        ).exists()

        if not is_member:
            return False

        if view.action in ["update", "partial_update"]:
            return self._can_update(role_name)

        if view.action == "destroy":
            return self._can_delete(role_name)

        return True

    def _get_permissions(self, role_name):
        return (
            Role.objects.filter(role_name=role_name)
            .values_list("access_rights", flat=True)
            .first()
            or []
        )

    def _can_update(self, role_name):
        access_rights = self._get_permissions(role_name)
        return 4 in access_rights

    def _can_delete(self, role_name):
        access_rights = self._get_permissions(role_name)
        return 5 in access_rights
