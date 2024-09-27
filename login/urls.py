from django.urls import path, include
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('accounts/', include('allauth.urls')), # New
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('', home_redirect_view, name='home_redirect'),
    path('<path:url>', home_redirect_view, name='catch_all'),
]