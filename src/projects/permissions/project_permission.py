from rest_framework.permissions import BasePermission

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models.project_member import ProjectMember
from projects.models.role import Role


class ProjectPermission(BasePermission):
    """
    Кастомный пермишен для проверки прав доступа к проектам.
    """

    def has_permission(self, request, view):
        """
        Проверка доступа на уровне запроса
        (например, доступ к списку проектов).
        """
        user_id, role_name, _ = decode_jwt_token(request)
        request.user_id = user_id
        request.role_name = role_name

        if role_name == "admin":
            return True

        match view.action:
            case "create":
                return self._can_create(role_name)
            case "update":
                return self._can_update(role_name)
            case "delete":
                return self._can_delete(role_name)

        return True

    def has_object_permission(self, request, view, obj):
        """
        Проверка доступа на уровне объекта
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

        if view.action == "create":
            return self._can_create(role_name)

        if view.action in ["update", "partial_update"]:
            return self._can_update(role_name)

        if view.action == "destroy":
            return self._can_delete(role_name)

        return True

    def _can_create(self, role_name):
        access_rights = self._get_permissions(role_name)
        return 3 in access_rights

    def _can_update(self, role_name):
        access_rights = self._get_permissions(role_name)
        return 4 in access_rights

    def _can_delete(self, role_name):
        access_rights = self._get_permissions(role_name)
        return 5 in access_rights

    def _get_permissions(self, role_name):
        return (
            Role.objects.filter(role_name=role_name)
            .values_list("access_rights", flat=True)
            .first()
            or []
        )
