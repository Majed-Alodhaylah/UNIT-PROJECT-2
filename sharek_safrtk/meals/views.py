from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Meal
from .forms import MealForm
from django.contrib.auth.models import User

def meals_list(request):
    query = request.GET.get('q')
    if query:
        meals = Meal.objects.filter(title__icontains=query)
    else:
        meals = Meal.objects.all()
    return render(request, 'meals/meals_list.html', {'meals': meals})


@login_required
def add_meal(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.owner = request.user
            meal.status = 'pending'  
            meal.save()
            messages.success(request, "Meal added successfully!")
            return redirect('volunteer_dashboard')
    else:
        form = MealForm()
    return render(request, 'meals/meal_form.html', {'form': form})


@login_required
def delete_meal(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, owner=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, "Meal deleted successfully.")
        return redirect('volunteer_dashboard')
    return render(request, 'meals/meal_confirm_delete.html', {'meal': meal})


@login_required
def volunteer_dashboard(request):
    meals = Meal.objects.filter(owner=request.user)
    return render(request, 'users/volunteer_dashboard.html', {'meals': meals})


@login_required
def association_dashboard(request):
    meals = Meal.objects.filter(status='pending')
    return render(request, 'users/association_dashboard.html', {'meals': meals})


@login_required
def update_meal_status(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    if request.method == 'POST':
        action = request.POST.get('action')  
        comment = request.POST.get('comment', '')

        if action == 'accept':
            meal.status = 'accepted'
            meal.accepted_by = request.user
            meal.comment_from_association = comment
            meal.save()
            messages.success(request, "Meal accepted successfully.")
        elif action == 'reject':
            meal.status = 'rejected'
            meal.accepted_by = request.user
            meal.comment_from_association = comment
            meal.save()
            messages.warning(request, "Meal rejected.")
        return redirect('association_dashboard')
    return redirect('association_dashboard')
