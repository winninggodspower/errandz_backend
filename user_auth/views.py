from django.shortcuts import render, get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Rider, Customer, Vendor, Account
from .serializers import RiderRegisterSerializer, CustomerRegisterSerializer, VendorRegisterSerializer, AccountSerializer, ProfileImageSerializer
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


class RegisterVendorView(generics.CreateAPIView, generics.UpdateAPIView):
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
    parser_classes = [FormParser, MultiPartParser]

    ACCOUNT_TYPE_MODEL_SERIALIZER = {
        'rider': RiderRegisterSerializer,
        'customer': CustomerRegisterSerializer,
        'vendor': VendorRegisterSerializer,
    }

    def get(self, request):
        account = request.user  # getting the account model

        # get the serialized data of the account type
        account_type_serializer = self.get_account_type_serialized_data(
            account, request)

        return Response(account_type_serializer.data, status=200)

    def get_account_type_serialized_data(self, account, request):
        model = account.get_account_type_instance()
        serializer_class = self.get_account_type_serializer(account.user_type)

        # returning user serialized information when method is get
        if request.method == "GET":
            serializer = serializer_class(model, context={'request': request})

        # passing user inputed data to serializer when method is PATCH
        elif request.method == "PATCH":
            serializer = serializer_class(
                instance=model, data=request.data, partial=True, context={'request': request})

        return serializer

    def get_account_type_serializer(self, account_type):
        return self.ACCOUNT_TYPE_MODEL_SERIALIZER.get(account_type)

    def patch(self, request):
        account = request.user  # getting the user model

        # get the account type serializer
        account_type_serializer = self.get_account_type_serialized_data(
            account, request)

        # validating user input
        account_type_serializer.is_valid(raise_exception=True)

        # saving the data
        account_type_serializer.save()

        return Response(account_type_serializer.data, status=status.HTTP_200_OK)


class AccountDetailId(AccountDetail):

    def get(self, request, pk):
        data = {}
        # getting the account model
        account = get_object_or_404(Account, pk=pk)

        # get account type model serializer instance and passing in account model
        account_type_serializer = self.get_account_type_serialized_data(
            account)

        return Response(account_type_serializer.data, status=200)


class ChangeProfileImageApiView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = ProfileImageSerializer
    queryset = Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)

    def patch(self, request, format=None):
        user = request.user

        serializer = ProfileImageSerializer(instance=user, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=200)
