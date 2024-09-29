from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm

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