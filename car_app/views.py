from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from .models import Vehicle

class VehicleListView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the list of vehicles
        vehicles = Vehicle.objects.all().values()

        # Convert the queryset to a list and return as JSON response
        return JsonResponse(list(vehicles), safe=False)
