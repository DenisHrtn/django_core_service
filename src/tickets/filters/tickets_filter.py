import django_filters

from tickets.models import Ticket


class TicketFilter(django_filters.FilterSet):
    """
    Кастомный фильтр для фильтрации тикетов
    """

    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    assignee = django_filters.NumberFilter(
        field_name="assignee_ids", lookup_expr="contains"
    )

    class Meta:
        model = Ticket
        fields = ["status", "project", "assignee"]
