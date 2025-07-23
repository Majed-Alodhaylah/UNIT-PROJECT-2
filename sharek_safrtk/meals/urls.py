from django.urls import path
from . import views

urlpatterns = [
    path('', views.meals_list, name='meals_list'),
]
