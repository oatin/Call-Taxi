from django.db import models
from django.contrib.auth.models import User as AuthUser

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location({self.latitude}, {self.longitude})"
    
class Ride(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    driver = models.ForeignKey('TaxiDriver', on_delete=models.SET_NULL, null=True, blank=True)
    start_location = models.ForeignKey(Location, related_name='start_locations', on_delete=models.CASCADE)
    end_location = models.ForeignKey(Location, related_name='end_locations', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # e.g., 'requested', 'in_progress', 'completed'
    request_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ride({self.id}, User: {self.user}, Driver: {self.driver})"

class TaxiDriver(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    car_model = models.CharField(max_length=100)
    car_plate = models.CharField(max_length=20)
    status = models.CharField(max_length=20)  # e.g., 'available', 'busy'

    def __str__(self):
        return f"TaxiDriver({self.user.username}, License: {self.license_number})"