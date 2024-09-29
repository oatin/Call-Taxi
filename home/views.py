from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Location, TaxiDriver
from django.contrib.auth import update_session_auth_hash

@login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        if request.user.role == "driver": 
            return redirect('home-taxi') 
        else:
            drivers = TaxiDriver.objects.select_related('current_location').all()
            context = {
                'drivers': drivers,
            }
            return render(request, 'home_page/index.html', context)

@login_required(login_url='/')
def home_taxi(request):
    if request.user.is_authenticated:
        if request.user.role == "driver":  
            return render(request, 'home_page/taxi.html')
        else:
            return redirect('home') 
        

def edit_profile(request):
    if request.method == 'POST':
        user = request.user

        # Update user information
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')  

        password = request.POST.get('password')
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user) 

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('home')  

    return render(request, 'profile.html')  