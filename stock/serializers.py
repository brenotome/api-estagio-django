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