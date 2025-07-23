from django.db import models
from django.contrib.auth.models import User
from meals.models import Meal

class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    stars = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.meal.title} - {self.stars} stars"
