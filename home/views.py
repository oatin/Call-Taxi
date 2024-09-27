from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Location, TaxiDriver
from django.views.decorators.http import require_GET
import json

@login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        if request.user.role == "driver":  # เปลี่ยนเป็น 'driver'
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
        if request.user.role == "driver":  # เปลี่ยนเป็น 'driver'
            return render(request, 'home_page/taxi.html')
        else:
            return redirect('home') 