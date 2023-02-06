from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRider, IsCustomer, IsNotificationOwner
import json

from .models import Delivery, Notification, History
from .serializers import DeliverySerializer, NotificationSerializer, AcceptDeliveryRequestSerializer, HistorySerializer
from .Paystack import PayStack
from .signals import check_payment_verified

# Create your views here.

class DeliveryView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        data = serializer.save(customer=self.request.user.get_account_type_instance())
    
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        delivery_model = get_object_or_404(Delivery, ref=response.data.get('ref'))

        # setting model checkout url
        checkout_url = PayStack().generate_checkout_url(delivery_model)
        
        delivery_model.checkout_url = checkout_url 
        delivery_model.save()
        
        data = {**response.data, 'checkout_url': checkout_url}
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request):
        delivery = Delivery.objects.filter(customer=request.user.customer).all()
        serializer = self.serializer_class(delivery, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SuccessfulDeliveryView(APIView):

    def post(self, request):
        ref = request.data.get("reference")
        delivery_model = get_object_or_404(Delivery, ref=ref)
        check_payment_verified(delivery_model)
        return Response(request.data, status=200)

    def get(self,  request):
        ref = request.query_params.get('ref')
        delivery_model = get_object_or_404(Delivery, ref=ref)
        check_payment_verified(delivery_model)
        return redirect('https://errandz-frontend.vercel.app/login')

class NotificationView(generics.RetrieveAPIView):
    queryset = Notification
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsNotificationOwner]

    def retrieve(self, request, *args, **kwargs):
        notification_model = Notification.objects.filter(account=request.user).all()
        
        if not notification_model:
            return Response({
                'message': 'notification empty'
            }, status=status.HTTP_200_OK)

        serializer = self.serializer_class(notification_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptDeliveryRequestView(APIView):
    permission_classes = [IsRider]

    def post(self, request):
        serializer = AcceptDeliveryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rider = request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    query_set = History.objects.all()

    def get(self, request):
        user_history_models = self.query_set.filter(account=request.user).all()
        serializer = HistorySerializer(user_history_models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
