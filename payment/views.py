from django.shortcuts import render
from .serializers import RiderPickupEarningSerializer, AccountDetailsSerializer
from .models import RiderPickupEarning, AccountDetail
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from delivery.permissions import IsRider
from rest_framework.response import Response
from rest_framework.decorators import api_view
from delivery.Paystack import PayStack

# Create your views here.

class RiderEarningView(generics.GenericAPIView):
    queryset = RiderPickupEarning.objects.all()
    serializer_class = RiderPickupEarningSerializer
    permission_classes = [IsRider]

    def get(self, request):
        model = self.get_queryset().filter(rider=request.user.rider)
        serializer = self.get_serializer(model, many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def get_bank_list(request):
    paystack = PayStack()
    status, result = paystack.get_bank_list()
    return Response(result)

class AccountDetailView(generics.CreateAPIView):
    queryset = AccountDetail.objects.all()
    serializer_class = AccountDetailsSerializer
    permission_classes = [IsRider]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rider=request.user.rider)
        return Response(serializer.data)