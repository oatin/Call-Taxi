from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('accounts/', include('allauth.urls')), # New
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', home_redirect_view, name='home_redirect'),

    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('<path:url>', home_redirect_view, name='catch_all'),
]