"""
URL configuration for sharek_safrtk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: 
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('meals/', include('meals.urls')),
    path('users/', include('users.urls')),
    path('charities/', TemplateView.as_view(template_name='charities/index.html'), name='charities_index'),
    path('volunteers/', TemplateView.as_view(template_name='volunteers/list.html'), name='volunteers_list'),
    path('meals/list/', TemplateView.as_view(template_name='meals/list.html'), name='meals_list'),


]

