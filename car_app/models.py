from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

#Getting the owner of the vehicle
def get_default_owner():
    try:
        return get_user_model().objects.get(username='admin')
    except get_user_model().DoesNotExist:
        return None

#User model
class MyUser(AbstractUser):
    position = models.CharField(max_length=50, blank = True, null= False)
    img = models.ImageField(upload_to='user-images', null=True)
    email = models.EmailField(unique=True)

#Vehicle model
class Vehicle(models.Model):

    FUEL_CHOICES = [
        ('Benzin', 'Benzin'),
        ('Dizel', 'Dizel'),
        ('Električno', 'Električno'),
        ('Hibrid', 'Hibrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('Automatik', 'Automatik'),
        ('Manual', 'Manual'),
        ('DSG' , 'DSG'),
    ]

    SEAT_CHOICES = [
        ('2', '2'),
        ('4', '4'),
        ('5','5'),
        ('6','6'),
        ('7','7'),
        ('11', '11'),
    ]
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('denied', 'denied'),
    ]

    BODY_CHOICES = [
        ('Limuzina', 'Limuzina'),
        ('SUV','SUV'),
        ('Karavan', 'Karavan'),
        ('Kupe', 'Kupe'),
        ('Kabriolet', 'Kabriolet'),
    ]

    image = models.ImageField(upload_to='vehicle_images', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    video_url = models.URLField(null=True)
    vehicle_make = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    car_body = models.CharField(max_length=15, choices=BODY_CHOICES, default='Limuuzina')
    year_of_manufacturing = models.PositiveIntegerField()
    description = models.CharField(max_length=500, blank=True)
    fuel_type = models.CharField(max_length=100, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=100, choices=TRANSMISSION_CHOICES)
    door_count = models.PositiveIntegerField()
    seat_number = models.IntegerField(default=5, choices = SEAT_CHOICES)
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        default=get_default_owner
    )

#Gallery model
class VehicleGallery(models.Model):
    image = models.ImageField(upload_to = 'vehicle_images', null=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='gallery'
    )