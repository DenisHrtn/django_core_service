from rest_framework.permissions import BasePermission

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models import ProjectMember, Role
from tickets.models import Ticket


class TicketPermission(BasePermission):
    """
    Кастомный пермишен для проверки доступа к таске.
    Если пользователь имеет роль на уровне проекта,
    то ему разрещается только читать таску.
    Админ видит все таски и может манипулировать ими.
    Участники таски могут выполнить любые действия с ней.
    Удалять таску может только админ.
    """

    def has_permission(self, request, view):
        """
        Проверка доступа на уровне запроса.
        """
        user_id, role_name, _ = decode_jwt_token(request)
        request.user_id = user_id
        request.role_name = role_name

        if role_name == "admin":
            return True

        match view.action:
            case "list":
                return self._can_view(user_id)
            case "create":
                return self._can_create(role_name)
            case "update":
                return self._can_update(user_id)
            case "delete":
                return self._can_delete(role_name)

    def has_object_permission(self, request, view, obj):
        """
        Проверка доступа на уровне объекта
        """
        user_id = request.user_id
        role_name = request.role_name

        if role_name == "admin":
            return True

        is_member = ProjectMember.objects.filter(
            project_id=obj.project.project_id, user_id=user_id
        ).exists()

        if not is_member:
            return False

        if view.action == "list":
            return self._can_view(user_id)

        if view.action == "partial_update":
            return self._can_update(role_name)

        if view.action == "destroy":
            return self._can_delete(role_name)

    def _can_view(self, user_id):
        is_assignee = Ticket.objects.filter(assignee_ids__contains=[user_id])
        if not is_assignee:
            return False
        return True

    def _can_create(self, role_name):
        access_rights = self._get_permissions(role_name)
        return any(right in access_rights for right in [3])

    def _can_update(self, user_id):
        is_assignee = Ticket.objects.filter(assignee_ids__contains=[user_id])
        if not is_assignee:
            return False
        return True

    def _can_delete(self, role_name):
        if role_name == "admin":
            return True
        return False

    def _get_permissions(self, role_name):
        return (
            Role.objects.filter(role_name=role_name)
            .values_list("access_rights", flat=True)
            .first()
            or []
        )
