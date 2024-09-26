from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import CustomSignupForm

# Create your views here.
def catch_all_view(request, url):
    if request.user.is_authenticated:
        if request.user.role == "คนขับ":
            return redirect('home') 
        else:
            return redirect('home-taxi') 
    else:
        return redirect('/')

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # เปลี่ยน URL ไปที่หน้า login หรือหน้าอื่นที่ต้องการ
    else:
        form = CustomSignupForm()
    return render(request, 'allauth/account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # หรือหน้าที่คุณต้องการให้ redirect หลัง login
        else:
            # ส่งข้อความผิดพลาดกลับไปยัง template
            return render(request, 'login_page/login.html', {'error': 'Invalid credentials'})
    return render(request, 'login_page/login.html')
