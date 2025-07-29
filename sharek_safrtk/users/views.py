from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import Profile
from meals.models import Meal


def is_user_type(user, role):
    return hasattr(user, 'profile') and user.profile.user_type == role


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
            if is_user_type(user, 'volunteer'):
                return redirect('volunteer_dashboard')
            elif is_user_type(user, 'association'):
                return redirect('association_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Incorrect username or password.")
    return render(request, 'users/login.html')


@login_required
def volunteer_dashboard(request):
    if not is_user_type(request.user, 'volunteer'):
        return redirect('home')

    meals = request.user.meals_owned.select_related('accepted_by').all()
    return render(request, 'users/volunteer_dashboard.html', {'meals': meals})


@login_required
def association_dashboard(request):
    if not is_user_type(request.user, 'association'):
        return redirect('home')

    pending_meals = Meal.objects.filter(status='pending')
    accepted_meals = Meal.objects.filter(status='accepted', accepted_by=request.user)

    return render(request, 'users/association_dashboard.html', {
        'pending_meals': pending_meals,
        'accepted_meals': accepted_meals,
        'accepted_count': accepted_meals.count(),
    })


@login_required
def accept_meal(request, meal_id):
    if not is_user_type(request.user, 'association'):
        return redirect('home')

    meal = get_object_or_404(Meal, id=meal_id)
    meal.status = 'accepted'
    meal.available = False
    meal.accepted_by = request.user
    meal.save()
    messages.success(request, "Meal accepted successfully!")
    return redirect('association_dashboard')


@login_required
def association_reports(request):
    if not is_user_type(request.user, 'association'):
        return redirect('home')

    status_filter = request.GET.get('status')
    meals = Meal.objects.all()
    if status_filter in ['pending', 'accepted', 'rejected']:
        meals = meals.filter(status=status_filter)

    volunteers = User.objects.filter(profile__user_type='volunteer')

    return render(request, 'users/association_reports.html', {
        'volunteers_count': volunteers.count(),
        'meals': meals,
        'status_filter': status_filter,
    })


@login_required
def update_meal_status(request, meal_id):
    if not is_user_type(request.user, 'association'):
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('home')

    meal = get_object_or_404(Meal, id=meal_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')

        if action in ['accept', 'reject']:
            meal.status = 'accepted' if action == 'accept' else 'rejected'
            meal.accepted_by = request.user
            meal.comment_from_association = comment
            meal.available = False if action == 'accept' else meal.available
            meal.save()
            messages.success(request, f"Meal {action}ed successfully!")

    return redirect('association_dashboard')
