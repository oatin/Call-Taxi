from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import redirect

# Create your views here.
def catch_all_view(request, url):
    if request.user.is_authenticated:
        return redirect('home')  # redirect ไปยังหน้า home ถ้าล็อกอินแล้ว
    else:
        return redirect('/')
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/home')  # ถ้าผู้ใช้ล็อกอินแล้ว redirect ไปที่ /home
    return TemplateView.as_view(template_name='login_page/login.html')(request)