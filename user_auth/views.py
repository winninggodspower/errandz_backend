from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Rider, Customer, Vendor, Account
from .serializers import RiderRegisterSerializer, CustomerRegisterSerializer, VendorRegisterSerializer, AccountSerializer
from rest_framework.permissions import IsAuthenticated

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


class AccountDetail(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    ACCOUNT_TYPE_MODEL_SERIALIZER = {
        'rider': RiderRegisterSerializer,
        'customer': CustomerRegisterSerializer,
        'vendor': VendorRegisterSerializer,
    }

    def get(self, request):
        data = {}
        account = request.user # getting the account model

        account_type_serializer = self.get_account_type_serialized_data(account) # get account type model serializer instance and passing in account model

        return Response(account_type_serializer.data, status=200)

    def get_account_type_serialized_data(self, account):
        model = account.get_account_type_instance()
        serializer_class = self.get_account_type_serializer(account.user_type)
        serializer = serializer_class(model)
        return serializer

    
    def get_account_type_serializer(self, account_type):
        return self.ACCOUNT_TYPE_MODEL_SERIALIZER.get(account_type)





