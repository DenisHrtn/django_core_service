import uuid
from typing import Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpRequest
from rest_framework.exceptions import NotFound, ValidationError

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models import Invite, Project, ProjectMember, Role
from projects.tasks import send_invite_token_to_email


class ProjectInviteService:
    """
    Сервис для работы с приглашениями на проект
    """

    @staticmethod
    def generate_invite_token():
        """
        Метод для генерации токена приглашения
        """
        invite_token = uuid.uuid4()
        return invite_token

    @staticmethod
    def get_all_invites(user_id: int, project_id: int, role_name: str) -> List[Invite]:
        """
        Метод для получения всех инвайтов в конкретном проекте
        :param role_name: str
        :param project_id: int
        :param user_id: int
        :return: list[Invite]
        """
        if role_name == "admin":
            return Invite.objects.select_related("project").filter(
                project_id=project_id
            )

        project_ids = ProjectMember.objects.filter(user_id=user_id).values_list(
            "project_id", flat=True
        )
        invites = Invite.objects.filter(project_id__in=project_ids)

        return invites

    @staticmethod
    def get_invite_by_id(invite_id: int) -> Optional[Invite]:
        """
        Метод для получения инвайта
        :param invite_id: int
        :return: invite if any
        """
        try:
            return (
                Invite.objects.select_related("project")
                .filter(invite_id=invite_id)
                .first()
            )
        except ObjectDoesNotExist as exc:
            raise NotFound("Инвайт не найден") from exc

    @staticmethod
    def send_invite(data: Dict[str, str], project_id: int) -> Dict[str, str]:
        """
        Создание и отправка инвайта
        :param data: dict
        :param project_id: int
        :return: new invite
        """
        email = data["email"]
        token = str(ProjectInviteService.generate_invite_token())

        if Invite.objects.filter(email=email).exists():
            raise ValidationError("Приглашение для такого email уже существует!")

        project = Project.objects.filter(project_id=project_id).first()

        with transaction.atomic():
            send_invite_token_to_email.delay(
                to_address=email,
                token=token,
                project_name=project.name,
            )

            new_invite = Invite.objects.create(
                email=email, project=project, token=token
            )

            return {"id": new_invite.invite_id}

    @staticmethod
    def accept_invite(
        token: str, invite_response: bool, request: HttpRequest
    ) -> Dict[str, str]:
        """
        Метод для принятия инвайта.
        Пользователь может отклонить инвайт или принять его.
        :param token: str
        :param invite_response: bool
        :param request: HttpRequest
        :return:
        """
        user_id, role_name, email = decode_jwt_token(request=request)

        role_access_rights = (
            Role.objects.filter(role_name=role_name)
            .values_list("access_rights", flat=True)
            .first()
        )

        invite = Invite.objects.filter(email=email).first()

        if not invite:
            raise ObjectDoesNotExist("Инвайта с таким ID не существует")

        errors = []
        if invite.status != "pending":
            errors.append("Инвайт уже принят или отклонен!")
        if invite.token != token:
            errors.append("Токены не совпадают!")

        if errors:
            raise ValidationError(errors)

        with transaction.atomic():
            if invite_response is True:
                invite.status = "accepted"

                project_member = ProjectMember.objects.create(
                    project_id=invite.project,
                    user_id=user_id,
                    email=invite.email,
                    access_rights=role_access_rights,
                )
            else:
                invite.status = "rejected"

            invite.save()

            return {
                "detail": f"Инвайт {invite.invite_id}\n\n"
                f"был отмечен со статусом {invite.status}\n"
                f"и создан новый мембер {project_member}"
            }
