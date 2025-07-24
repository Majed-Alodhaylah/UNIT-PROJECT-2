from django.urls import path
from . import views

urlpatterns = [
    path('', views.meals_list, name='meals_list'),
    path('add/', views.add_meal, name='add_meal'),
]
