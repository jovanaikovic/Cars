from rest_framework import serializers
from car_app.models import Vehicle
from car_app.models import MyUser

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "image",
            "vehicle_make",
            "vehicle_model",
            "year_of_manufacturing",
            "description",
            "fuel_type",
            "transmission",
            "door_count",
            "vehicle_price",
            "seat_number",
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

