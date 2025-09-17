from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from .models import Poll
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Poll)
def schedule_poll_results_calculation(sender, instance, created, **kwargs):
    """
    Schedule the result calculation task to run after the poll ends
    """
    if created or instance.end_time > timezone.now():
        try:
            # Try to import and use Celery if available
            from .tasks import calculate_poll_results
            
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
            logger.info(f"Scheduled poll results calculation for poll {instance.id}")
            
        except Exception as e:
            # If Celery is not available, log the error and continue
            logger.warning(f"Could not schedule poll results calculation: {str(e)}")
            logger.info("Poll results will need to be calculated manually or when Celery is available")
            
            # In production, you might want to:
            # 1. Store the poll ID in a database table for manual processing
            # 2. Send an alert to administrators
            # 3. Use a different task scheduling mechanism