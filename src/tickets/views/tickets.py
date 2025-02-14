from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions.text import Lower
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from tickets.filters.tickets_filter import TicketFilter
from tickets.models import Ticket
from tickets.permissions.tickets_permission import TicketPermission
from tickets.serializers.ticket_serializer import (
    AssigneeActionSerializer,
    TicketSerializer,
)
from tickets.services.ticket_service import TicketService


class TicketReadOnlyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    Ручка для GET-запросов по задачам

    Сортировка:
        1. Чтобы отсортировать по названию (по убыванию):
        http://127.0.0.1:8000/api/tickets/tickets/10/?ordering=-title_lower
    """

    permission_classes = [TicketPermission]
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    queryset = Ticket.objects.all()
    filterset_class = TicketFilter
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")

        return TicketService.get_all_tickets(project_id=project_id).annotate(
            title_lower=Lower("title")
        )

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        ticket_id = self.kwargs.get("ticket_id")

        try:
            return TicketService.get_ticket_by_id(
                project_id=project_id, ticket_id=ticket_id
            )
        except ObjectDoesNotExist as exc:
            raise NotFound("Задача не найдена!") from exc


class TicketCreateViewSet(GenericViewSet):
    """
    Ручка для создания таски
    """

    permission_classes = [TicketPermission]
    serializer_class = TicketSerializer

    def create(self, request, *args, **kwargs):
        project_id = kwargs.get("project_id")

        ticket = TicketService.create_new_ticket(
            project_id=project_id, data=request.data, request=request
        )

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=201)


class AddAssigneeToTicketViewSet(GenericViewSet):
    """
    Ручка для добавления участника в задачу
    """

    permission_classes = [TicketPermission]
    serializer_class = AssigneeActionSerializer
    queryset = Ticket.objects.all()

    def partial_update(self, request, *args, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        project_id = kwargs.get("project_id")
        user_id = request.data.get("user_id")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = TicketService.add_assignee_to_ticket(
            project_id=project_id, ticket_id=ticket_id, user_id=int(user_id)
        )

        return Response(result, status=200)


class RemoveAssigneeFromTicketViewSet(GenericViewSet):
    """
    Ручка для удаления участника из задачи
    """

    permission_classes = [TicketPermission]
    serializer_class = AssigneeActionSerializer
    queryset = Ticket.objects.all()

    def partial_update(self, request, *args, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        project_id = kwargs.get("project_id")
        user_id = request.data.get("user_id")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = TicketService.remove_assignee_from_ticket(
            project_id=project_id, ticket_id=ticket_id, user_id=int(user_id)
        )

        return Response(result, status=200)


class UpdateTicketViewSet(UpdateModelMixin, GenericViewSet):
    """
    Ручка для обновления задач
    """

    permission_classes = [TicketPermission]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        ticket_id = self.kwargs.get("ticket_id")

        try:
            return TicketService.get_ticket_by_id(
                project_id=project_id, ticket_id=ticket_id
            )
        except ObjectDoesNotExist as exc:
            raise NotFound("Задача не найдена!") from exc


class DeleteTicketViewSet(DestroyModelMixin, GenericViewSet):
    """
    Ручка для удаления задачи
    """

    permission_classes = [TicketPermission]
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_object(self):
        project_id = self.kwargs.get("project_id")
        ticket_id = self.kwargs.get("ticket_id")

        try:
            return TicketService.get_ticket_by_id(
                project_id=project_id, ticket_id=ticket_id
            )
        except ObjectDoesNotExist as exc:
            raise NotFound("Задача не найдена!") from exc
