from rest_framework import viewsets
from .serializers import *
from register.models import *
from rest_framework.response import Response


class SimOrderViewSet(viewsets.ModelViewSet):
    queryset = SimOrder.objects.all()
    serializer_class = SimOrderSerializer

class SimCardOptionViewSet(viewsets.ModelViewSet):
    queryset = SimCardOption.objects.all()
    serializer_class = SimCardOptionSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
