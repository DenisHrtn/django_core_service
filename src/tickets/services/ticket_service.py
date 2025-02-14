from datetime import timedelta
from typing import Dict, List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpRequest
from rest_framework.exceptions import PermissionDenied

from common_services.utils.decode_jwt_token import decode_jwt_token
from projects.models import ProjectMember
from projects.services.project_members_service import ProjectMembersService
from projects.services.project_service import ProjectService
from tickets.models import Ticket, TicketNotification
from tickets.serializers.ticket_serializer import TicketSerializer


class TicketService:
    """
    Сервис для работы с тасками
    """

    @staticmethod
    def get_all_tickets(project_id: int) -> List[Ticket]:
        """
        Получения всех тасок в конкретном проекте
        :param project_id: int
        :return: tickets if any
        """
        project = ProjectService.get_project_by_id(project_id=project_id)

        tickets = project.tickets.all()

        return tickets

    @staticmethod
    def get_ticket_by_id(ticket_id: int, project_id: int) -> Optional[Ticket]:
        """
        Получаем конкретный тикет по ID
        :param ticket_id: int
        :param project_id: int
        :return: ticket if any
        """
        project = ProjectService.get_project_by_id(project_id=project_id)

        ticket = project.tickets.filter(ticket_id=ticket_id).first()

        if not ticket:
            raise ObjectDoesNotExist(f"Задача с ID {ticket_id} не найдена")

        return ticket

    @staticmethod
    def create_new_ticket(
        project_id: int,
        data: Dict,
        request: HttpRequest,
    ) -> Optional[Ticket]:
        """
        Создание таски
        :param project_id: int
        :param data: dict
        :param request: HttpRequest
        :return: ticket
        """
        user_id, role_name, email = decode_jwt_token(request)

        project = ProjectService.get_project_by_id(project_id=project_id)

        is_member = ProjectMember.objects.filter(
            user_id=user_id, project_id=project_id
        ).exists()

        if not (is_member or role_name == "admin"):
            raise PermissionDenied("Вы не являетесь участником этого проекта.")

        serializer = TicketSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            new_ticket = serializer.save(project=project, creator=email)
            return new_ticket

    @staticmethod
    def add_assignee_to_ticket(
        project_id: int, ticket_id: int, user_id: int
    ) -> Dict[str, str]:
        """
        Добавление участника проекта на таску
        :param project_id: int
        :param ticket_id: int
        :param user_id: int
        :return: dict
        """
        project = ProjectService.get_project_by_id(project_id=project_id)
        ticket = TicketService.get_ticket_by_id(
            ticket_id=ticket_id, project_id=project_id
        )

        is_project_member = ProjectMembersService.is_project_member(
            project_id=project.project_id, user_id=user_id
        )

        if not is_project_member:
            raise PermissionDenied(
                "Пользователь не является участником данного проекта!"
            )

        project_members = ProjectMember.objects.filter(project_id=project_id)

        project_member = project_members.get(user_id=user_id)
        project_member_email = project_member.email

        with transaction.atomic():
            if user_id not in ticket.assignee_ids:
                ticket.assignee_ids.append(user_id)
                ticket.save(update_fields=["assignee_ids"])

                notify_time = ticket.due_date - timedelta(hours=1)

                TicketNotification.objects.create(
                    ticket=ticket,
                    assignee_email=project_member_email,
                    notify_time=notify_time,
                )

                return {"detail": f"Юзер с ID {user_id} был успешно добавлен в задачу!"}

            return {"detail": f"Юзер с ID {user_id} уже добавлен в задачу!"}

    @staticmethod
    def remove_assignee_from_ticket(
        project_id: int, ticket_id: int, user_id: int
    ) -> Dict[str, str]:
        """
        Метод для удаления участника с задачи
        :param project_id: int
        :param ticket_id: int
        :param user_id: int
        :return: dict
        """
        project = ProjectService.get_project_by_id(project_id=project_id)
        ticket = TicketService.get_ticket_by_id(
            ticket_id=ticket_id, project_id=project_id
        )

        is_project_member = ProjectMembersService.is_project_member(
            project_id=project.project_id, user_id=user_id
        )

        if not is_project_member:
            raise PermissionDenied(
                "Пользователь не является участником данного проекта!"
            )

        if user_id in ticket.assignee_ids:
            ticket.assignee_ids.remove(user_id)
            ticket.save(update_fields=["assignee_ids"])
            return {"detail": f"Юзер с ID {user_id} был успешно удален из задачи!"}

        return {"detail": f"Юзер с ID {user_id} не является участником задачи!"}
