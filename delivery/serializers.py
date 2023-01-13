from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'customer', 'pickup_location', 'recipient_name', 'recipient_email', 'recipient_phone_number', 'delivery_location', 'recievers_name', 'receivers_email', 'receiver_phone_number', 'goods_description']