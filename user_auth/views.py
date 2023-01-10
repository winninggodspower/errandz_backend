from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import generics
from .models import Rider, Customer, Vendor
from .serializers import RiderRegisterSerializer, CustomerRegisterSerializer, VendorRegisterSerializer

# Create your views here.

class RegisterRiderView(generics.CreateAPIView):
    query_set = Rider.objects.all()
    serializer_class = RiderRegisterSerializer
    

    def post(self, request):
        serializer = RiderRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class RegisterCustomerView(generics.CreateAPIView):
    query_set = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


class RegisterVendorView(generics.CreateAPIView):
    query_set = Vendor.objects.all()
    serializer_class = VendorRegisterSerializer
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)