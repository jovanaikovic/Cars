from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



class MyUser(AbstractUser):
    pass

class Vehicle(models.Model):

    FUEL_CHOICES = [
        ('Benzin', 'Benzin'),
        ('Dizel', 'Dizel'),
        ('Električno', 'Električno'),
        # Add more choices as needed
    ]

    TRANSMISSION_CHOICES = [
        ('Automatik', 'Automatik'),
        ('Manual', 'Manual'),
        ('DSG' , 'DSG'),
        # Add more choices as needed
    ]
    superuser = get_user_model().objects.get(username='admin')

    vehicle_make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    year_of_manufacturing = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=100, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=100, choices=TRANSMISSION_CHOICES)
    door_count = models.PositiveIntegerField()
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, default=superuser)
