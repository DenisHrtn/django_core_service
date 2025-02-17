from django.urls import path

from .views.tickets import (
    AddAssigneeToTicketViewSet,
    DeleteTicketViewSet,
    RemoveAssigneeFromTicketViewSet,
    TicketCreateViewSet,
    TicketReadOnlyViewSet,
    UpdateTicketViewSet,
)

urlpatterns = [
    path(
        "tickets/<int:project_id>/",
        TicketReadOnlyViewSet.as_view({"get": "list"}),
        name="tickets-list",
    ),
    path(
        "tickets/<int:project_id>/ticket/<int:ticket_id>/",
        TicketReadOnlyViewSet.as_view({"get": "retrieve"}),
        name="tickets-detail",
    ),
    path(
        "tickets/<int:project_id>/ticket-create/",
        TicketCreateViewSet.as_view({"post": "create"}),
        name="tickets-create",
    ),
    path(
        "tickets/<int:project_id>/add-assignee-to-ticket/<int:ticket_id>/",
        AddAssigneeToTicketViewSet.as_view({"patch": "partial_update"}),
        name="tickets-add-assignee-to-ticket",
    ),
    path(
        "tickets/<int:project_id>/remove-assignee-from-ticket/<int:ticket_id>/",
        RemoveAssigneeFromTicketViewSet.as_view({"patch": "partial_update"}),
        name="tickets-remove-assignee-from-ticket",
    ),
    path(
        "tickets/<int:project_id>/ticket-update/<int:ticket_id>/",
        UpdateTicketViewSet.as_view({"patch": "partial_update"}),
        name="tickets-update",
    ),
    path(
        "tickets/<int:project_id>/ticket-delete/<int:ticket_id>/",
        DeleteTicketViewSet.as_view({"delete": "destroy"}),
        name="tickets-delete",
    ),
]
