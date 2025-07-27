from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('volunteer/dashboard/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('association/dashboard/', views.association_dashboard, name='association_dashboard'),
    path('association/update_meal/<int:meal_id>/', views.update_meal_status, name='update_meal_status'),
    path('association/reports/', views.association_reports, name='association_reports'),
]
