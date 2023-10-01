"""
URL configuration for car_sales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenVerifyView
from car_app.views import VehicleList, NewestCarsView, AdminPageView
from car_app.views import VehicleDetail, UserListView, UserCreateView, VehicleCreateView
from car_app.views import UserDetail
from django.contrib.auth import views as auth_views



urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('cheapest-car', CheapestCarView.as_view(), name = 'cheapest-car'),
    path('', NewestCarsView.as_view(), name='newest-cars'),
    path("api-auth/", include("rest_framework.urls")),
    #Token url-s
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #-----------
    path('cars/', VehicleList.as_view(), name='vehicle-list'),
    path('car/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('admin/', AdminPageView.as_view(), name='admin-page'),
    path('admin/users/', UserListView.as_view(), name='admin-user-list'),
    path('admin/users/create/', UserCreateView.as_view(), name='admin-user-create'),
    path('cars/create', VehicleCreateView.as_view(), name='vehicle-list'),
]

