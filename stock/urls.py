from django.urls import path, include
from . import views
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('users',views.UserView)
router.register('products',views.ProductView)
router.register('orders',views.OrderView)


urlpatterns = [
    path('',include(router.urls))
]