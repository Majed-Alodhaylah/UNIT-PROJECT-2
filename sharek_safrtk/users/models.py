from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPES = [
        ('volunteer', 'Volunteer'),
        ('association', 'Association'),  
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
