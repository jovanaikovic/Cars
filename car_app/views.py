from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .models import Vehicle
from .serializers import VehicleSerializer
from .serializers import MyUserSerializer
from .models import MyUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

class CheapestCarView(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all().order_by('vehicle_price').first()  # Retrieve the car with the lowest price
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'pk'
    def get_object(self):
        return self.queryset 

class NewestCarsView(generics.ListAPIView):
    queryset = Vehicle.objects.all().order_by('-id')[:10]  # Retrieve the 10 newest cars
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VehicleList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication] 
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VehicleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VehicleDetail(APIView):
    authentication_classes = [SessionAuthentication] 
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
    
class UserList(APIView):
    def get(self, request):
        users = MyUser.objects.all()
        serializer = MyUserSerializer(users, many=True)
        return Response(serializer.data)
    
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

class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to create new users.")

        return super().create(request, *args, **kwargs)


