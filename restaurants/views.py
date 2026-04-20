from django.shortcuts import render
from rest_framework import generics
from .models import Restaurant
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serializers import RestaurantSerializer
# Create your views here.
class RestaurantListAPIVIEW(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]