from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

from .models import Comment


@receiver(post_save, sender=Comment)
def notification_on_create_comment(sender, instance, created, **kwargs):
    if created:
        # Update last active field in the parent ticket
        instance.ticket.last_active = timezone.now()
        instance.ticket.save()

        print '[comment created] Send email to submitter: %s' % (instance.ticket.submitter)

        if instance.ticket.agent:
            print '[comment created] Send email to agent: %s' % (instance.ticket.agent)
