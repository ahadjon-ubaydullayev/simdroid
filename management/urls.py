from django.urls import path, include
from rest_framework import routers
from .import tableviews as tableview
from .import views


router = routers.DefaultRouter()
router.register('order', viewset=tableview.SimOrderViewSet)
router.register('client', viewset=tableview.ClientViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('orders/', views.orders, name='orders'),
    path('clients/', views.clients, name='clients'),
    path('<int:id>/', views.order_detail, name="order_detail"),
    
]
