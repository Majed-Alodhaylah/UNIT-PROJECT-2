from django.shortcuts import render, redirect
from .models import Meal
from .forms import MealForm
from django.contrib.auth.decorators import login_required

def meals_list(request):
    meals = Meal.objects.all()
    return render(request, 'meals/meals_list.html', {'meals': meals})

@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.owner = request.user
            meal.save()
            return redirect('meals_list')
    else:
        form = MealForm()
    return render(request, 'meals/meal_form.html', {'form': form})
