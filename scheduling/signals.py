from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Schedule


@receiver(pre_save, sender=Schedule)
def auto_update_schedule_status(sender, instance, **kwargs):
    """
    Automatically transition schedule status based on current time.
    Only applies to confirmed schedules — cancelled ones are left alone.
    """
    if instance.status == Schedule.CANCELLED:
        return

    now = timezone.now()

    if instance.start_datetime and instance.end_datetime:
        if now >= instance.end_datetime:
            instance.status = Schedule.COMPLETED
        elif now >= instance.start_datetime:
            instance.status = Schedule.ONGOING