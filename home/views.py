from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Location, TaxiDriver, Ride
from django.contrib.auth import update_session_auth_hash

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from math import radians, sin, cos, sqrt, atan2
import json

def haversine(lon1, lat1, lon2, lat2):
    R = 6371  # Radius of the Earth in kilometers
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def create_ride_request(request):
    driver_id = request.POST.get('driver_id')

    try:
        driver = TaxiDriver.objects.get(id=driver_id)

        start_location = Location.objects.get(user=request.user)

        existing_ride = Ride.objects.filter(passenger=request.user, status__in=['requested', 'accepted', 'driver_arrived', 'in_progress'])

        if existing_ride.exists():
            existing_ride.delete()

        Ride.objects.create(
            passenger=request.user,
            driver=driver,
            start_location=start_location,
            status='requested'
        )

        messages.success(request, 'Ride request sent successfully!')

    except TaxiDriver.DoesNotExist:
        messages.error(request, 'Driver not found')
    except Location.DoesNotExist:
        messages.error(request, 'Start location not found')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return redirect('home')
    
@login_required
def save_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            location = Location.objects.get(user=request.user)
            location.latitude = latitude
            location.longitude = longitude
            location.save()
        except Location.DoesNotExist:
            location = Location.objects.create(user=request.user, latitude=latitude, longitude=longitude)

        try:
            taxi_driver = TaxiDriver.objects.get(user=request.user)
            taxi_driver.current_location = location
            taxi_driver.save()
        except TaxiDriver.DoesNotExist:
            pass  

        return JsonResponse({'success': True, 'location': str(location)})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required(login_url='/')
def home(request):
    if request.user.is_authenticated:
        if request.user.role == "driver": 
            return redirect('home-taxi') 
        else:
            if Location.objects.filter(user=request.user).exists():
                driver_distances = []
                user_location = Location.objects.get(user=request.user)
                job_requests = Ride.objects.filter(passenger=request.user).order_by('-request_time')
                user_lat = user_location.latitude
                user_lon = user_location.longitude
                
                drivers = TaxiDriver.objects.select_related('current_location').all()
                for driver in drivers:
                        driver_location = driver.current_location
                        if driver_location:
                            distance = haversine(user_lon, user_lat, driver_location.longitude, driver_location.latitude)
                            driver_distances.append((driver, distance))
                
                closest_drivers = sorted(driver_distances, key=lambda x: x[1])[:3]
                context = {
                    'drivers': drivers,
                    'closest_drivers': [driver for driver, _ in closest_drivers],
                    'job_requests': job_requests,
                }
                return render(request, 'home_page/index.html', context)
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
            job_requests = Ride.objects.filter(driver__user=request.user)

            context = {
                'job_requests': job_requests
            }
            return render(request, 'home_page/taxi.html', context)
        else:
            return redirect('home')
        
@login_required(login_url='/')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user

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

    return redirect('home')  

@login_required(login_url='/')
def job_request(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action:  
            job_id = action.split('_')[1] 
            try:
                ride = Ride.objects.get(id=job_id) 
                
                if action.startswith('accept'): 
                    ride.status = "accepted"
                elif action.startswith('decline'):  
                    ride.status = "cancelled" 
                
                ride.save()
            except Ride.DoesNotExist:
                pass

        return redirect('home') 

    return redirect('home')