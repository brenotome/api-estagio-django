from rest_framework import serializers, status
from django.conf import settings
from .models import Order,Product,User
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','username','password','email','first_name','last_name','address')
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate_password(self, value: str) -> str:
        return make_password(value)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','price','date','stock')
        read_only_fields = ['date']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','price','stock')

class OrderReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    class Meta:
        model = Order
        fields = ('id','product','user','quantity','total_price','paid')
        read_only_fields = ['total_price','paid']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','product','user','quantity','total_price','paid')
        read_only_fields = ['total_price','paid','user']

    def create(self, validated_data):
        order = Order(
            user=self.context['request'].user,
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
            product.stock += order.quantity
            order.quantity = validated_data['quantity']
            order.total_price = order.quantity * order.product.price
            order.save()
            product.stock -= order.quantity
            product.save()
            return order
        else:
            raise serializers.ValidationError("Out of Stock")