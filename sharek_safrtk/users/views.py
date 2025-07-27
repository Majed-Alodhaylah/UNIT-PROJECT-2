from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import Profile
from meals.models import Meal


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                user_type=form.cleaned_data['user_type'],
                phone=form.cleaned_data.get('phone', ''),
                address=form.cleaned_data.get('address', ''),
            )
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'profile'):
                if user.profile.user_type == 'volunteer':
                    return redirect('volunteer_dashboard')
                elif user.profile.user_type == 'association':
                    return redirect('association_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
    return render(request, 'users/login.html')


@login_required
def volunteer_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'volunteer':
        return redirect('home')
    meals = request.user.meals_owned.all()
    return render(request, 'users/volunteer_dashboard.html', {'meals': meals})


@login_required
def association_dashboard(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'association':
        return redirect('home')
    meals = Meal.objects.filter(status='pending')  
    return render(request, 'users/association_dashboard.html', {'meals': meals})


@login_required
def accept_meal(request, meal_id):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'association':
        return redirect('home')

    meal = get_object_or_404(Meal, id=meal_id)
    meal.available = False
    meal.status = 'accepted'
    meal.accepted_by = request.user
    meal.save()
    messages.success(request, "Meal accepted successfully!")
    return redirect('association_dashboard')


@login_required
def association_reports(request):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'association':
        return redirect('home')
    volunteers = User.objects.filter(profile__user_type='volunteer')
    meals = Meal.objects.all()
    return render(request, 'users/association_reports.html', {
        'volunteers_count': volunteers.count(),
        'meals': meals,
    })


@login_required
def update_meal_status(request, meal_id):
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'association':
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        action = request.POST.get('action')  
        comment = request.POST.get('comment', '')

        if action == 'accept':
            meal.status = 'accepted'
            meal.accepted_by = request.user
            meal.comment_from_association = comment
            meal.save()
            messages.success(request, "Meal accepted successfully!")
        elif action == 'reject':
            meal.status = 'rejected'
            meal.accepted_by = request.user
            meal.comment_from_association = comment
            meal.save()
            messages.warning(request, "Meal rejected.")
        return redirect('association_dashboard')

    return redirect('association_dashboard')
