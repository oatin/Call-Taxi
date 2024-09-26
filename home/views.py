from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Location, TaxiDriver

@login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        if request.user.role == "driver":  # เปลี่ยนเป็น 'driver'
            return redirect('home-taxi') 
        else:
            return render(request, 'home_page/index.html')

@login_required(login_url='/')
def home_taxi(request):
    if request.user.is_authenticated:
        if request.user.role == "driver":  # เปลี่ยนเป็น 'driver'
            return render(request, 'home_page/taxi.html')
        else:
            return redirect('home') 
        
def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude and longitude:  
            location = Location(user=request.user, latitude=latitude, longitude=longitude)
            location.save()
        else:
            return render(request, 'home_page/index.html', {'error': 'Both latitude and longitude are required.'})

    return render(request, 'home_page/index.html')

def taxi_locations(request):
    available_drivers = TaxiDriver.objects.filter(status='Available')
    locations = []
    for driver in available_drivers:
        if driver.current_location:
            locations.append({
                'latitude': driver.current_location.latitude,
                'longitude': driver.current_location.longitude,
                'driver_name': driver.user.username,
                'icon': 'img/taxi-svgrepo-com.svg', 
            })
    return JsonResponse(locations, safe=False)