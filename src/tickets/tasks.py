import logging

from celery import shared_task
from django.utils import timezone

from common_services.services.email_service import send_email_via_ses

from .models import TicketNotification

logger = logging.getLogger(__name__)


@shared_task
def send_ticket_notification():
    now = timezone.now()

    try:
        notifications = TicketNotification.objects.filter(
            notify_time__lte=now,
            sent=False,
            ticket__due_date__gte=now + timezone.timedelta(hours=1),
        )

        for notification in notifications:
            send_email_via_ses.apply_async(
                args=[
                    f"Напоминание о задаче: {notification.ticket.title}",
                    f"У вас есть задача с дедлайном: {notification.ticket.due_date}.",
                    notification.assignee_email,
                ]
            )

            notification.sent = True
            notification.save()

            logger.info(
                f"Notification sent to {notification.assignee_email}"
                f" for ticket {notification.ticket.title}."
            )

    except Exception as e:
        logger.error(f"Error while sending ticket notifications: {e}")
