from rest_framework import serializers
from car_app.models import Vehicle
from car_app.models import MyUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "image",
            "vehicle_make",
            "vehicle_model",
            "car_body",
            "year_of_manufacturing",
            "description",
            "fuel_type",
            "transmission",
            "door_count",
            "vehicle_price",
            "seat_number",
            "owner",
            "video_url",
            "status",
        ]

class MyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.ReadOnlyField()

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "password", "is_superuser", "position", "img"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)

