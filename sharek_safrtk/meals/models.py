from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),       
        ('accepted', 'Accepted'),     
        ('delivered', 'Delivered'),   
        ('rejected', 'Rejected'),    
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meals_owned'
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='meals/', blank=True, null=True)
    available = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    accepted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meals_accepted'
    )

    comment_from_association = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.owner.username}"
