from rest_framework import serializers, status
from django.conf import settings
from .models import Order,Product,User
from rest_framework.response import Response


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User #settings.AUTH_USER_MODEL
        fields = ('id','url','username','password','email','first_name','last_name','address')
        extra_kwargs = {
            'password':{'write_only':True}
        }

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id','url','name','description','price','date','stock')
        read_only_fields = ['date']
        # extra_kwargs = {
        #     'creation_date':{'read_only':True}
        # }

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id','url','product','user','quantity','total_price','paid')
        read_only_fields = ['total_price','paid']

    def create(self, validated_data):
        order = Order(
            user=validated_data['user'],
            product=validated_data['product'],
            quantity=validated_data['quantity'],
            paid = False,
        )
        order.total_price = order.quantity * order.product.price
        if(order.quantity <= order.product.stock):
            order.save()
            product = order.product
            product.stock -= order.quantity
            product.save()
            return order
        else:
            raise serializers.ValidationError("Out of Stock")
    
    def update(self,instance, validated_data):
        order = instance
        product = order.product
        if(validated_data['quantity'] <= product.stock+order.quantity):
            product.quantity += product.stock
            order.quantity = validated_data['quantity']
            order.total_price = order.quantity * order.product.price
            order.save()
            product.stock -= order.quantity
            product.save()
            return order
        else:
            raise serializers.ValidationError("Out of Stock")
    
    def delete(self, pk):
        order = Order.objects.get(pk=pk)
        product = order.product
        product.stock += order.quantity
        product.save()
        order.delete()
