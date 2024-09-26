from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# Create your views here.
def catch_all_view(request, url):
    if request.user.is_authenticated:
        return redirect('home')  # redirect ไปยังหน้า home ถ้าล็อกอินแล้ว
    else:
        return redirect('/')
    
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
