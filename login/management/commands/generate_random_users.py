import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.models import TaxiDriver, Location  # Adjust 'yourapp' to your app name

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate random taxi drivers and locations'

    def handle(self, *args, **kwargs):
        for i in range(75,100):  # Change this number for more or fewer users
            # Create a random user
            username = f'driver_{i}'
            password = '1'  # You can use a more secure password
            user = User.objects.create_user(username=username, password=password, is_driver=True, role='driver')

            # Create a random location
            latitude = random.uniform(13, 14)  # Random latitude
            longitude = random.uniform(99, 101)  # Random longitude
            location = Location.objects.create(user=user, latitude=latitude, longitude=longitude)

            # Create a taxi driver
            TaxiDriver.objects.create(
                user=user,
                license_number=f'LICENSE_{i}',
                car_model=f'Car Model {i}',
                car_plate=f'XYZ-{i}',
                status=random.choice(['available', 'busy', 'offline']),
                current_location=location
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created driver: {username}'))

