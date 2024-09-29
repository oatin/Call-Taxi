from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'), # New
    path('taxi/', views.home_taxi, name='home-taxi'), # New
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('save-location/', views.save_location, name='save_location'),
    path('job_request/', views.job_request, name='job_request'),
    path('create_ride_request/', views.create_ride_request, name='create_ride_request'),
]