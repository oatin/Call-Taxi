# Generated by Django 5.1 on 2024-09-26 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_ride'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxiDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('car_model', models.CharField(max_length=100)),
                ('car_plate', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('busy', 'Busy'), ('offline', 'Offline')], max_length=20)),
                ('current_location', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.location')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rides_as_driver', to='home.taxidriver'),
        ),
    ]
