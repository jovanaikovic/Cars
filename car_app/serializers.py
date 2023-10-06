import imghdr
from django.forms import ValidationError
from rest_framework import serializers
from car_app.models import Vehicle, VehicleGallery
from car_app.models import MyUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def validate_image(value):
    # Check if the uploaded file is a valid image (PNG or JPEG)
    valid_types = ('png', 'jpeg')
    image_type = imghdr.what(None, h=value.read())
    
    if image_type not in valid_types:
        raise ValidationError("Only PNG and JPEG images are supported.")

class VehicleSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validate_image])
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
    
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_superuser'] = user.is_superuser

        return token
    
class VehicleGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model =  VehicleGallery
        fields = [
            "image",
            "id",
        ]
        def validate(self, data):
        # Ensure that the number of images is at most 5
            vehicle_id = self.context['view'].kwargs.get('pk')
            existing_images = VehicleGallery.objects.filter(vehicle__id=vehicle_id)
        
            if existing_images.count() >= 5:
                raise serializers.ValidationError("Cannot add more than 5 images for a vehicle.")
        
            return data

