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
                "project_id": project_id,
                "owner_id": owner_id,
                "created_at": created_at,
                "updated_at": updated_at,
            }
        )

        send_event(event="project_events", key=str(project_id), value=data)

    @staticmethod
    def send_project_member_event(
        project_id: int,
        user_id: int,
    ):
        data = json.dumps(
            {
                "project_id": project_id,
                "user_id": user_id,
            }
        )

        send_event(event="project_member_events", key=str(project_id), value=data)

    @staticmethod
    def send_ticket_event(
        ticket_id: int,
        project_id: int,
        status: str,
        creator: str,
        assignee_ids: list,
        due_date: datetime,
    ):
        data = json.dumps(
            {
                "event_type": "ticket_created",
                "ticket_id": ticket_id,
                "project_id": project_id,
                "status": status,
                "creator": creator,
                "assignee_ids": assignee_ids,
                "due_date": due_date.isoformat() if due_date else None,
            }
        )

        send_event("ticket_topic", key=str(ticket_id), value=data)

    @staticmethod
    def send_ticket_status_change(
        ticket_id: int, project_id: int, old_status: str, new_status: str
    ):
        data = json.dumps(
            {
                "event_type": "ticket_status_changed",
                "ticket_id": ticket_id,
                "project_id": project_id,
                "old_status": old_status,
                "new_status": new_status,
            }
        )

        send_event("change_status_topic", key=str(ticket_id), value=data)
