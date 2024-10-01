from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import timedelta
from home.models import TaxiDriver, Location, Ride
from login.models import CustomUser

class Command(BaseCommand):
    help = 'Generates mock data for the taxi app'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        # Create users
        for _ in range(100):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                phone_number=fake.phone_number(),
                is_driver=random.choice([True, False]),
                role='driver' if random.choice([True, False]) else 'passenger'
            )
            
            Location.objects.create(
                user=user,
                latitude=fake.latitude(),
                longitude=fake.longitude()
            )

        # Create taxi drivers
        drivers = User.objects.filter(is_driver=True)
        for driver in drivers:
            TaxiDriver.objects.create(
                user=driver,
                license_number=fake.uuid4(),
                car_model=fake.vehicle_make_model(),
                car_plate=fake.license_plate(),
                status=random.choice(['available', 'busy', 'offline'])
            )

        # Create rides
        passengers = User.objects.filter(is_driver=False)
        drivers = TaxiDriver.objects.all()
        
        for _ in range(500):
            start_time = fake.date_time_between(start_date='-30d', end_date='now')
            end_time = start_time + timedelta(minutes=random.randint(10, 120))
            
            Ride.objects.create(
                passenger=random.choice(passengers),
                driver=random.choice(drivers),
                start_location=Location.objects.create(
                    user=random.choice(passengers),
                    latitude=fake.latitude(),
                    longitude=fake.longitude()
                ),
                end_location=Location.objects.create(
                    user=random.choice(passengers),
                    latitude=fake.latitude(),
                    longitude=fake.longitude()
                ),
                request_time=start_time,
                start_time=start_time,
                end_time=end_time,
                status=random.choice(['completed', 'cancelled', 'in_progress']),
                fare=random.uniform(10, 100)
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated mock data'))