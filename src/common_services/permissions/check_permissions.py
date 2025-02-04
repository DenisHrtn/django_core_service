from rest_framework.permissions import BasePermission

from projects.models.role import Role


class PermissionCheck(BasePermission):
    """
    Класс для проверки разрешений на работу с проектами
    """

    def __init__(self, role_name: str):
        self.role_name = role_name
        self.permissions = (
            Role.objects.filter(role_name=self.role_name)
            .values_list("permissions", flat=True)
            .first()
        )

    def is_admin(self):
        return self.role_name == "admin"

    def can_create(self):
        if self.permissions and 3 in self.permissions or self.is_admin():
            return True
        return False

    def can_update(self):
        if self.permissions and 4 in self.permissions or self.is_admin():
            return True
        return False

    def can_delete(self):
        if self.permissions and 5 in self.permissions or self.is_admin():
            return True
        return False
