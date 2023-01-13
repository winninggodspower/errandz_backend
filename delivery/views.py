from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics

from .models import Delivery
from .serializers import DeliverySerializer

# Create your views here.

class DeliveryView(generics.CreateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
