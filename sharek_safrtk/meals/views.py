from django.shortcuts import render
from .models import Meal

def meals_list(request):
    meals = Meal.objects.all()
    return render(request, 'meals/meals_list.html', {'meals': meals})
