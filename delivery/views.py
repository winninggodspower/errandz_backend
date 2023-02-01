from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRider, IsCustomer, IsNotificationOwner

from .models import Delivery, Notification
from .serializers import DeliverySerializer, NotificationSerializer, AcceptDeliveryRequestSerializer

# Create your views here.

class DeliveryView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.get_account_type_instance())


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