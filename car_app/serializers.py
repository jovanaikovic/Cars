from rest_framework import serializers
from car_app.models import Vehicle
from car_app.models import MyUser

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "vehicle_make",
            "vehicle_model",
            "year_of_manufacturing",
            "description",
            "fuel_type",
            "transmission",
            "door_count",
            "vehicle_price",
            "owner",
        ]

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            
        ]
