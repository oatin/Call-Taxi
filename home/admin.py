from django.contrib import admin
from .models import *

admin.site.register(TaxiDriver)
admin.site.register(Ride)
admin.site.register(Location)