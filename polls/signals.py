from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Poll
from .tasks import calculate_poll_results
from datetime import timedelta

@receiver(post_save, sender=Poll)
def schedule_poll_results_calculation(sender, instance, created, **kwargs):
    """
    Schedule the result calculation task to run after the poll ends
    """
    if created or instance.end_time > timezone.now():
        # Calculate when the poll will end
        end_time = instance.start_time + timedelta(hours=instance.duration)
        
        # Schedule the task to run at the end time
        # We use countdown to specify the number of seconds until execution
        seconds_until_end = max(0, (end_time - timezone.now()).total_seconds())
        
        # Schedule the task
        calculate_poll_results.apply_async(
            args=[instance.id],
            countdown=int(seconds_until_end)
        )