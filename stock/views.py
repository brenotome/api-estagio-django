from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from django.conf import settings

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer