from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, serializers
from .models import Vehicle, MyUser
from .serializers import VehicleSerializer, MyUserSerializer, CustomTokenSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from PIL import Image
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

# #Cheapest car for the right side banner, url cars/cheapest DONE!!!!!!!!!!!!
class CheapestVehicleView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        # Retrieve the cheapest car based on vehicle_price
        cheapest_car = Vehicle.objects.filter(status='approved').order_by('vehicle_price').first()

        if cheapest_car is not None:
            serializer = VehicleSerializer(cheapest_car)
            return Response(serializer.data)
        else:
            return Response({'detail': 'No approved cars available'}, status=status.HTTP_404_NOT_FOUND)
# #----------------------------------------

#Newest 10 cars for the home page slider, url /cars/newest DONE!!!!!!!!!!!!!
class NewestVehicleView(generics.ListAPIView):
    queryset = Vehicle.objects.filter(status='approved').order_by('-id')[:10]
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
#----------------------------------------

#All cars created on the website, url /cars, DONE!!!!!!!!!!!!!!!
class VehicleList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = VehicleSerializer

    def get_queryset(self):
        # Retrieve filter parameters from the request
        fuel_type = self.request.query_params.get('fuel_type', None)
        transmission = self.request.query_params.get('transmission', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        seat_number = self.request.query_params.get('seat_number', None)
        year_of_manufacturing = self.request.query_params.get('year_of_manufacturing', None)
        car_body = self.request.query_params.get('car_body', None)

        # Start with all vehicles
        queryset = Vehicle.objects.filter(status = 'approved')

        # Apply filters based on parameters
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        if min_price and max_price:
            queryset = queryset.filter(vehicle_price__range=(min_price, max_price))
        if seat_number:
            queryset = queryset.filter(seat_number = seat_number)
        if year_of_manufacturing:
            queryset = queryset.filter(year_of_manufacturing = year_of_manufacturing)
        if car_body:
            queryset = queryset.filter(car_body = car_body)
        return queryset

#---------------------------------------------

#Vehicle details, who created it and patch / delete options, unauthorized is read only, DONE!!!!!
class VehicleDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        vehicle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#------------------------------------

#Shows all cars one user created, should be a full user view to return also the data about the user itself.
#Should be invisible to non authorized user.  DONE!!!!!!!!!!!!
class UserDetail(APIView):
    def get(self, request, pk):
        try:
            user = MyUser.objects.get(pk=pk)   
            # Check if the user making the request is the superadmin or the owner of the profile
            if not request.user.is_superuser and request.user != user:
                raise PermissionDenied("You don't have permission to view this user's details.")
            user_serializer = MyUserSerializer(user)          
            # Check if the requested user is the same as the logged-in user
            is_own_profile = request.user == user
            vehicles = Vehicle.objects.filter(owner=user)
            vehicle_serializer = VehicleSerializer(vehicles, many=True)
            response_data = {
                'user': user_serializer.data,
                'vehicles': vehicle_serializer.data,
            }
            # Include additional user information if it's the own profile
            if is_own_profile:
                response_data['is_own_profile'] = True
            return Response(response_data)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to delete users.")
        return super().delete(request, *args, **kwargs)
    def patch(self, request, pk):
        try:
            user = MyUser.objects.get(pk=pk)
            # Check if the user making the request is the superadmin or the owner of the profile
            if not request.user.is_superuser and request.user != user:
                raise PermissionDenied("You don't have permission to update this user's profile.")
            
            # If the request data contains 'password', hash it before saving
            if 'password' in request.data:
                request.data['password'] = make_password(request.data['password'])
            
            serializer = MyUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
#-------------------------------------------

#Not sure why it was necesarry, but will check
class AdminPageView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to access this view.")
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
#---------------------------------------------

#List of all users, should be visible only to logged in users, on normal
#users list admin shouldnt be visible DONE!!!!!!!!!!!!!!!!!
class UserListView(ListAPIView):
    serializer_class = MyUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Only return non-superuser users for regular users
        if not self.request.user.is_superuser:
            return get_user_model().objects.filter(is_superuser=False)
        
        # Return all users for superusers
        return get_user_model().objects.all()
#---------------------------------------------

#User creation for admin    DONE!!!!!!!!!!!!!!!!!!
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to create new users.")

        return super().create(request, *args, **kwargs)
#----------------------------------------------
    
#Creates a vehicle, DONE!!!!!!!!!!!!
class VehicleCreateView(generics.CreateAPIView):
    serializer_class = VehicleSerializer

    def perform_create(self, serializer):
        # Automatically set the owner to the currently logged-in user
        serializer.save(owner=self.request.user)
#----------------------------------------------

#View for vehicle approval, DONE!!!!!!!!
class ApproveVehiclesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, pk):
        # Retrieve the vehicle with the specified pk and status 'pending'
        try:
            vehicle = Vehicle.objects.get(pk=pk, status='pending')
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        # Check if the requester is a superuser
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to change vehicle status.")

        try:
            vehicle = Vehicle.objects.get(pk=pk, status='pending')
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Update the status based on the request data
        new_status = request.data.get('status', None)
        if new_status and new_status in ['approved', 'denied']:
            if new_status == 'denied':
                # Delete the vehicle if status is 'denied'
                vehicle.delete()
                return Response({"message": "Vehicle deleted due to denial."}, status=status.HTTP_200_OK)
            else:
                # Update status if 'approved'
                vehicle.status = new_status
                vehicle.save()
                serializer = VehicleSerializer(vehicle)
                return Response(serializer.data)
        else:
            return Response({"error": "Invalid status value. Use 'approved' or 'denied'."}, status=status.HTTP_400_BAD_REQUEST)
#-------------------------------------

#JPG Validator
class JPEGFileValidator:
    def __call__(self, value):
        try:
            image = Image.open(value)
            image.verify()  
        except Exception as e:
            raise serializers.ValidationError("Invalid image file. Please upload a valid JPEG photo.")
#--------------------------------------

#Vehicle image updater        
class UpdateVehicleImageView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    file_validator = JPEGFileValidator()

    def patch(self, request, pk):
        file = request.data.get("image")

        try:
            self.file_validator(file)
        except serializers.ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "File uploaded successfully."}, status=status.HTTP_200_OK)
#--------------------------------

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer
