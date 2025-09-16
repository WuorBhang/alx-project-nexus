from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model with role-based permissions
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        VOTER = 'VOTER', _('Voter')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VOTER,
    )
    
    # Additional fields can be added here
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    def is_voter(self):
        return self.role == self.Role.VOTER