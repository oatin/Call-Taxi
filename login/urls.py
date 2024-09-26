from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView # New
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.login_view, name='login'), # New
    path('accounts/', include('allauth.urls')), # New
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'), # New
    path('<path:url>', views.catch_all_view, name='catch_all'), # New
]