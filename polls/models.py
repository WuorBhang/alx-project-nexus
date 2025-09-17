from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Poll(models.Model):
    """
    Model for managing elections/polls
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title)
    
    @property
    def end_time(self):
        if self.start_time is None or self.duration is None:
            return None
        return self.start_time + timezone.timedelta(hours=self.duration)
    
    @property
    def is_active(self):
        if self.start_time is None or self.duration is None:
            return False
        now = timezone.now()
        end_time = self.end_time
        if end_time is None:
            return False
        return self.start_time <= now <= end_time
    
    @property
    def has_ended(self):
        if self.start_time is None or self.duration is None:
            return False
        end_time = self.end_time
        if end_time is None:
            return False
        return timezone.now() > end_time
    
    @property
    def status(self):
        if self.is_active:
            return "Active"
        elif self.has_ended:
            return "Ended"
        else:
            return "Upcoming"

class Position(models.Model):
    """
    Model for positions that candidates can run for
    """
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.poll.title}"

class Candidate(models.Model):
    """
    Model for candidates running for positions
    """
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='candidates/', blank=True, null=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.position.title}"
    
    @property
    def poll(self):
        """Get the poll through the position"""
        return self.position.poll

class Vote(models.Model):
    """
    Model to record votes cast by voters
    """
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='votes')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='votes')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensure a voter can only vote once per position
        unique_together = ('voter', 'position')
    
    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"
    
    @property
    def poll(self):
        """Get the poll through the position"""
        return self.position.poll
    
    def clean(self):
        # Ensure the candidate belongs to the specified position
        if self.candidate.position != self.position:
            raise ValidationError("Invalid candidate for the specified position.")
        
        # Ensure the poll is active
        if not self.poll.is_active:
            raise ValidationError("Voting is not allowed for this poll at this time.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)