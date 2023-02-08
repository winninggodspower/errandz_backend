from django.shortcuts import get_object_or_404
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from user_auth.models import Rider
from .models import Delivery, Notification, History
from user_auth.serializers import CustomerRegisterSerializer, RiderRegisterSerializer

class DeliverySerializer(serializers.ModelSerializer):
    recipient_phone_number  = PhoneNumberField(region="NG")
    receiver_phone_number   = PhoneNumberField(region="NG")
    customer                = CustomerRegisterSerializer(read_only=True)
    rider_who_accepted      = RiderRegisterSerializer(read_only=True)
    class Meta:
        model = Delivery
        fields = "__all__"

        extra_kwargs = {
                    'ref': {'read_only': True},
                    'status': {'read_only': True},
                    'checkout_url': {'read_only': True},
                    'has_driver_accepted_request': {'read_only': True},
        }


class NotificationSerializer(serializers.ModelSerializer):
    model = DeliverySerializer(read_only=True)
    class Meta:
        model = Notification
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'

def has_rider_accepted_request(delivery_ref):
    delivery_model = get_object_or_404(Delivery, ref=delivery_ref)
    if delivery_model.has_driver_accepted_request:
        raise serializers.ValidationError('Request with the ref has already been accepted')


class AcceptDeliveryRequestSerializer(serializers.Serializer):
    delivery_ref = serializers.UUIDField(validators=[has_rider_accepted_request])


    def save(self, account):
        delivery_ref = self.validated_data.get('delivery_ref')
        delivery_model = get_object_or_404(Delivery, ref=delivery_ref)
        
        # check if  payment has been made to request
        if delivery_model.status == delivery_model.STEPS.get(1):
            raise serializers.ValidationError({'details': 'delivery payment not verified'})

        return delivery_model.accept_request(account)
         
