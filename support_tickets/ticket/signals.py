from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from ..base.choices import TICKET_STATUS

from .models import Ticket


@receiver(post_save, sender=Ticket)
def notification_on_create_ticket(sender, instance, created, **kwargs):
    if created:
        print '[ticket created] Send email to submitter: %s' % (instance.submitter)

        if instance.agent:
            print '[ticket created] Send email to agent: %s' % (instance.agent)


@receiver(pre_save, sender=Ticket)
def notification_on_change_ticket(sender, instance, **kwargs):
    if instance.id:
        # Evaluate agent changes
        if instance.tracker.has_changed('agent'):
            if not instance.tracker.previous('agent'):
                print '[ticket modified] New agent'
            else:
                print '[ticket modified] Change agent'

        # Evaluate status changes
        if instance.tracker.has_changed('status'):
            if instance.status == TICKET_STATUS.closed:
                print '[ticket modified] Ticket closed'
