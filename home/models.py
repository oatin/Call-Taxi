from django.db import models
from login.models import *
from django.conf import settings

class Location(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s location"

    def __str__(self):
        return f"Location({self.latitude}, {self.longitude})"

class TaxiDriver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ])
    current_location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True, blank=True)  # เพิ่มฟิลด์นี้เพื่อเก็บตำแหน่งปัจจุบัน

    def __str__(self):
        return f"TaxiDriver({self.user.username}, License: {self.license_number})"
    
class Ride(models.Model):
    RIDE_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    passenger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='rides_as_passenger')
    driver = models.ForeignKey(TaxiDriver, on_delete=models.SET_NULL, null=True, related_name='rides_as_driver')
    start_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='rides_from')
    end_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='rides_to')
    request_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=RIDE_STATUS_CHOICES, default='requested')
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Ride {self.id}: {self.passenger.username} - {self.status}"
