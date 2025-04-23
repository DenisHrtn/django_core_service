from django.db.models.signals import pre_save
from django.dispatch import receiver

from common_services.kafka.event_driver import EventDriver

from .models.ticket import Ticket


@receiver(pre_save, sender=Ticket)
def track_ticket_status_change(sender, instance, **kwargs):
    if instance.pk:
        old_ticket = Ticket.objects.get(pk=instance.pk)
        if old_ticket.status != instance.status:
            EventDriver.send_ticket_status_change(
                ticket_id=instance.pk,
                project_id=instance.project.project_id,
                status=instance.status,
            )
