from django.shortcuts import render
from rest_framework import generics
from .models import Restaurant, RestaurantCategory
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serializers import RestaurantSerializer, RestaurantCategorySerializer


# Create your views here.
class RestaurantListAPIVIEW(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]

class RestaurantDetailAPIVIEW(generics.RetrieveAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'


class RestaurantMenuView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]

class RestaurantCategoryListView(generics.ListAPIView):
    serializer_class=RestaurantCategorySerializer
    queryset = RestaurantCategory.objects.all()
    permission_classes = [AllowAny]

class MenuCategoryListView(generics.ListAPIView):
    serializer_class=RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]

class MenuItemDetailView(generics.RetrieveAPIView):
    serializer_class=RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'id'






