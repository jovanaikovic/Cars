from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Vehicle, MyUser
from .serializers import VehicleSerializer, MyUserSerializer, CustomTokenSerializer, VehicleGallerySerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

#All vehicles on the web, with different filters for viewing different data according to needs
class VehicleList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = VehicleSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Retrieve filter parameters from the request
        fuel_type = self.request.query_params.get('fuel_type', None)
        transmission = self.request.query_params.get('transmission', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        seat_number = self.request.query_params.get('seat_number', None)
        year_of_manufacturing = self.request.query_params.get('year_of_manufacturing', None)
        car_body = self.request.query_params.get('car_body', None)
        status = self.request.query_params.get('status', None)
        owner_id = self.request.query_params.get('owner', None)

        # Start with all vehicles
        queryset = Vehicle.objects.all()

        # Apply filters based on parameters
        if fuel_type:
            queryset = queryset.filter(fuel_type=fuel_type)
        if transmission:
            queryset = queryset.filter(transmission=transmission)
        if min_price and max_price:
            queryset = queryset.filter(vehicle_price__range=(min_price, max_price))
        if seat_number:
            queryset = queryset.filter(seat_number=seat_number)
        if year_of_manufacturing:
            queryset = queryset.filter(year_of_manufacturing=year_of_manufacturing)
        if car_body:
            queryset = queryset.filter(car_body=car_body)
        # Apply status filter
        if status == 'pending':
            queryset = queryset.filter(status='pending')
        elif status == 'approved':
            queryset = queryset.filter(status='approved')
        if owner_id:
            queryset = queryset.filter(owner__id=owner_id)


        return queryset
    def get_cheapest_car(self):
        # Retrieve the cheapest car based on vehicle_price
        cheapest_car = Vehicle.objects.filter(status='approved').order_by('vehicle_price').first()
        return cheapest_car

    def get_newest_cars(self):
        # Retrieve the 10 newest cars based on id
        newest_cars = Vehicle.objects.filter(status='approved').order_by('-id')[:10]
        return newest_cars

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Check for specific query parameters
        if 'cheapest' in request.query_params:
            # Retrieve the cheapest car
            cheapest_car = self.get_cheapest_car()
            if cheapest_car is not None:
                serializer = self.serializer_class(cheapest_car)
                return Response(serializer.data)
            else:
                return Response({'detail': 'No approved cars available'}, status=status.HTTP_404_NOT_FOUND)

        elif 'newest' in request.query_params:
            # Retrieve the 10 newest cars
            newest_cars = self.get_newest_cars()
            serializer = self.serializer_class(newest_cars, many=True)
            return Response(serializer.data)

        else:
            # Default behavior for listing all cars with pagination
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        # Handle the creation of a new vehicle
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Set the owner to the currently logged-in user
            serializer.save(owner=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Vehicle details, getting the data of one vehicle at a time, including patch and delete functions
class VehicleDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def status_to_pending(self, data):
        # Set status to "pending" if the user is not an admin
        if not self.request.user.is_superuser:
            data['status'] = 'pending'

    def get_object(self, pk):
        try:
            return Vehicle.objects.get(pk=pk)
        except Vehicle.DoesNotExist:
            return None

    def get(self, request, pk):
        vehicle = self.get_object(pk)
        if vehicle:
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        vehicle = self.get_object(pk)
        if not vehicle:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the owner of the vehicle or an admin
        if request.user.is_superuser or request.user == vehicle.owner:
            if request.user.is_superuser:
                serializer = VehicleSerializer(vehicle, data=request.data, partial=True)
            # Allow updating all fields except status for authenticated users
            else:
                allowed_fields = ['image', 'vehicle_make', 'vehicle_model', 'car_body', 'year_of_manufacturing',
                              'description', 'fuel_type', 'transmission', 'door_count', 'seat_number', 'vehicle_price']
                if allowed_fields:
                    data = {key: value for key, value in request.data.items() if key in allowed_fields}
                    self.status_to_pending(data)
                else:
                    return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

                serializer = VehicleSerializer(vehicle, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'You do not have permission to perform this action.111111'}, status=status.HTTP_403_FORBIDDEN)
        

    def delete(self, request, pk):
        vehicle = self.get_object(pk)
        if not vehicle:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the user is an admin
        if request.user.is_superuser or request.user == vehicle.owner:
            vehicle.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

#User details, defined delete and patch user as well
class UserDetail(APIView):
    def get(self, request, pk):
        try:
            user = MyUser.objects.get(pk=pk)

            # Check if the user making the request is the superadmin or the owner of the profile
            if not request.user.is_superuser and not (request.user == user):
                raise PermissionDenied("You don't have permission to view this user's details.")

            user_serializer = MyUserSerializer(user)

            # Check if the requested user is the same as the logged-in user or if it's an admin
            is_own_profile = request.user == user or request.user.is_superuser

            # If the user is not an admin, filter vehicles by owner
            if request.user.is_superuser:
                vehicles = Vehicle.objects.all()
            else:
                vehicles = Vehicle.objects.filter(owner=user)

            vehicle_serializer = VehicleSerializer(vehicles, many=True)

            response_data = {
                'user': user_serializer.data,
                'vehicles': vehicle_serializer.data,
            }

            # Include additional user information if it's the own profile or if it's an admin
            if is_own_profile:
                response_data['is_own_profile'] = True

            return Response(response_data)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def delete(self, request, pk, *args, **kwargs):
        user = self.get_object(pk)

        # Check if the requester is a superuser or the owner of the profile
        if not request.user.is_superuser and request.user != user:
            raise PermissionDenied("You don't have permission to delete this user.")

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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

#List of all users that exist in the database, with create function only available to admin
class UserListView(ListAPIView):
    serializer_class = MyUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        # Only return non-superuser users for regular users
        if not self.request.user.is_superuser:
            return get_user_model().objects.filter(is_superuser=False)
        
        # Return all users for superusers
        return get_user_model().objects.all()

    def get_vehicle_count(self, user):
        # Return the count of vehicles created by the user
        return Vehicle.objects.filter(owner=user).count()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        
        # Get the count of vehicles for each user
        users_with_vehicle_count = []
        for user_data in serializer.data:
            user = get_user_model().objects.get(pk=user_data['id'])
            vehicle_count = self.get_vehicle_count(user)
            user_data['vehicle_count'] = vehicle_count
            users_with_vehicle_count.append(user_data)

        return Response(users_with_vehicle_count)
    
    def post(self, request, *args, **kwargs):
        # Handle the creation of a new user
        if not request.user.is_superuser:
            return Response("You don't have permission to create new users.")

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
    
#Custom token, sending is_superuser and user image with token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

#Gallery for the modal window
class GalleryView(generics.ListCreateAPIView):
    serializer_class = VehicleGallerySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        vehicle_id = self.kwargs.get('pk')
        return Vehicle.objects.get(pk=vehicle_id).gallery.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        vehicle_id = kwargs.get('pk')
        vehicle = Vehicle.objects.get(pk=vehicle_id)

        # Check if the user has permission to add images to this vehicle
        if request.user != vehicle.owner:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(vehicle=vehicle)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
