from django.urls import path
from . import views

urlpatterns = [
    path('', views.meals_list, name='meals_list'),
    path('add/', views.add_meal, name='add_meal'),
    path('delete/<int:meal_id>/', views.delete_meal, name='delete_meal'),
    path('update-status/<int:meal_id>/', views.update_meal_status, name='update_meal_status'),

]
