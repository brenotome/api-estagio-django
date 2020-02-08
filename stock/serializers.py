from rest_framework import serializers
from django.conf import settings
from .models import Order,Product,User

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
        fields = ('id','url','name','description','price','creation_date','stock')
        extra_kwargs = {
            'creation_date':{'read_only':True}
        }

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id','url','product','user','quantity','total_price','paid')