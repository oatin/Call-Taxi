from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # New
from django.contrib.auth.views import LogoutView


from . import views

urlpatterns = [
    path('', views.home, name='home'), # New
]