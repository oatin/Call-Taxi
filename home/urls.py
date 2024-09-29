from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'), # New
    path('taxi/', views.home_taxi, name='home-taxi'), # New
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]