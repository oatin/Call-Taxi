from django.contrib import admin
from .models import CustomUser, TaxiDriver

admin.site.register(CustomUser)
admin.site.register(TaxiDriver)