from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import CustomSignupForm

from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.urls import reverse_lazy

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get(self, request, *args, **kwargs):
        return redirect('login')  
    
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

def home_redirect_view(request, url=''):
    if request.user.is_authenticated:
        return redirect('home-taxi' if request.user.role != "คนขับ" else 'home')
    return redirect('login')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignupForm()
    
    return render(request, 'allauth/account/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    error_message = None 
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:   
            login(request, user)
            return redirect('home')
        else:
            error_message = 'รหัสผ่านหรือชื่อผู้ใช้ไม่ถูกต้อง'  
    
    return render(request, 'login_page/login.html', {'error': error_message})