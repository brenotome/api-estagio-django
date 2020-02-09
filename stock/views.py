from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, ProductListSerializer, OrderSerializer
from django.core import serializers

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['get'], name='orders')
    def orders(self,request,pk):
        user = self.get_object()
        orders = Order.objects.filter(user = user)
        return Response(list(orders.values()))

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self,request):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset,many=True)
        return Response(serializer.data)

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        order = self.get_object()
        product = order.product
        product.stock += order.quantity
        product.save()
        self.perform_destroy(order)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], name='pay')
    def pay(self,request,pk=None):
        order = self.get_object()
        order.paid = True
        order.save()
        return Response(self.get_serializer(order).data)
