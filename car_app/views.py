from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Vehicle
from .serializers import VehicleSerializer
from .serializers import MyUserSerializer
from .models import MyUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

# #Cheapest car for the right side banner, url cars/cheapest DONE!!!!!!!!!!!!
class CheapestVehicleView(APIView):
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

#Vehicle details, who created it and patch / delete options, unauthorized is read only
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
#Should be invisible to non authorized user.
class UserDetail(APIView):
    def get(self, request, pk):
        try:
            user = MyUser.objects.get(pk=pk)
            user_serializer = MyUserSerializer(user)
            vehicles = Vehicle.objects.filter(owner=user)
            vehicle_serializer = VehicleSerializer(vehicles, many=True)
            return Response({
                'vehicles': vehicle_serializer.data
            })
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to delete users.")
        return super().delete(request, *args, **kwargs)
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
#users list admin shouldnt be visible
class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser]
#---------------------------------------------

#User creation for admin
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to create new users.")

        return super().create(request, *args, **kwargs)
#----------------------------------------------
    
#Not sure if post will be defined here still, but staying for now
class VehicleCreateView(generics.CreateAPIView):
    serializer_class = VehicleSerializer

    def perform_create(self, serializer):
        # Automatically set the owner to the currently logged-in user
        serializer.save(owner=self.request.user)

    
    


