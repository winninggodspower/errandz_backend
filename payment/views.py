from django.shortcuts import render, get_object_or_404
from .serializers import RiderPickupEarningSerializer, AccountDetailsSerializer, RiderPaymentSerializer
from .models import RiderPickupEarning, AccountDetail
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from delivery.permissions import IsRider
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
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

class AccountDetailView(generics.ListCreateAPIView):
    queryset = AccountDetail.objects.all()
    serializer_class = AccountDetailsSerializer
    permission_classes = [IsRider]

    def post(self, request):
        if AccountDetail.objects.get(rider=request.user.rider):
            return Response({'message': 'account detial already exist for user'}, )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rider=request.user.rider)
        return Response(serializer.data)

    def get(self, request):
        model = get_object_or_404(AccountDetail, rider=request.user.rider)
        serializer = self.get_serializer(model)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        model = get_object_or_404(AccountDetail, rider=request.user.rider)
        serializer = self.get_serializer(model, data=request.data)
        serializer.is_valid(raise_exception=True)
        model = serializer.save(rider=request.user.rider)
        model.delete_recipient()
        return Response(serializer.data, status=status.HTTP_200_OK)
        
@api_view(['POST'])
@permission_classes([IsRider])
def rider_payment(request):
    serializer = RiderPaymentSerializer(data=request.data, context={'rider': request.user.rider})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data)