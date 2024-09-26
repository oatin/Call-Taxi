from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # New
from django.contrib.auth.views import LogoutView


from . import views

urlpatterns = [
    path('', views.home, name='home'), # New
    path('taxi/', views.home_taxi, name='home-taxi'), # New
    path('api/taxi-locations/', views.taxi_locations, name='taxi_locations'),
    path('save-location/', views.save_location, name='save_location'),
]