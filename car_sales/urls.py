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
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenRefreshView)
from rest_framework_simplejwt.views import TokenVerifyView
from car_app.views import VehicleList, AdminPageView, GalleryView
from car_app.views import VehicleDetail, UserListView, UpdateVehicleImageView
from car_app.views import CustomTokenObtainPairView, UserDetail, UpdateUserImageView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #Token url-s
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #-----------
    path("api-auth/", include("rest_framework.urls")),
    path('cars/', VehicleList.as_view(), name='vehicle-list'),
    path('cars/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('cars/<int:pk>/update_image/', UpdateVehicleImageView.as_view(), name='update_vehicle_image'),
    path('cars/<int:pk>/gallery/', GalleryView.as_view(), name='vehicle-gallery'),
    path('admin/', AdminPageView.as_view(), name='admin-page'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/update_image/', UpdateUserImageView.as_view(), name= 'update_user_image'),
    path('users/', UserListView.as_view(), name='admin-user-list'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

