import json
from datetime import datetime

from .send_event import send_event


class EventDriver:
    """
    Класс для отправки событий в Kafka
    """

    @staticmethod
    def send_project_event(
        project_id: int, owner_id: int, created_at: str, updated_at: str
    ):
        data = json.dumps(
            {
                "event_type": "project_event",
                "project_id": project_id,
                "owner_id": owner_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        send_event(event="analytics_topic", key=str("projects"), value=data)

    @staticmethod
    def send_project_member_event(
        project_id: int,
        user_id: int,
    ):
        data = json.dumps(
            {
                "event_type": "members_event",
                "project_id": project_id,
                "user_id": user_id,
            }
        )

        send_event(event="analytics_topic", key=str("project_members"), value=data)

    @staticmethod
    def send_ticket_event(
        ticket_id: int,
        project_id: int,
        status: str,
        creator: str,
        assignee_ids: list,
        created_at: datetime,
        due_date: datetime,
    ):
        data = json.dumps(
            {
                "event_type": "ticket_event",
                "ticket_id": ticket_id,
                "project_id": project_id,
                "status": status,
                "creator": creator,
                "assignee_ids": assignee_ids,
                "created_at": created_at.isoformat() if created_at else None,
                "due_date": due_date.isoformat() if due_date else None,
            }
        )

        send_event("analytics_topic", key=str("tickets"), value=data)

    @staticmethod
    def send_ticket_status_change(ticket_id: int, project_id: int, status: str):
        data = json.dumps(
            {
                "event_type": "ticket_status_change",
                "ticket_id": ticket_id,
                "project_id": project_id,
                "status": status,
            }
        )

        send_event("analytics_topic", key=str("tickets_statuses"), value=data)
