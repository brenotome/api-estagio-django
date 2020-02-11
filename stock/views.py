from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Product, Order
from .serializers import UserSerializer, ProductSerializer, ProductListSerializer, OrderSerializer, OrderReadSerializer
from stock.permissions import IsOwner, IsUser
from .pdf import PdfRender

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)
    
    def list(self,request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self,request):
        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset,many=True)
        return Response(serializer.data)

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def list(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderReadSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        print(pk)
        queryset = Order.objects.get(pk=pk)
        serializer = OrderReadSerializer(queryset)
        return Response(serializer.data)

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
        if not order.paid:
            order.paid = True
            order.save()
            return PdfRender.renderReceipt(self,order)
        else:
            return Response("Order already paid")
