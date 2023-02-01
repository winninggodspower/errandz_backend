from django.shortcuts import get_object_or_404
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Delivery, Notification

class DeliverySerializer(serializers.ModelSerializer):
    recipient_phone_number = PhoneNumberField(region="NG")
    receiver_phone_number = PhoneNumberField(region="NG")
    class Meta:
        model = Delivery
        fields = ['id', 'pickup_location', 'recipient_name', 'recipient_email', 'recipient_phone_number', 'delivery_location', 'recievers_name', 'receivers_email', 'receiver_phone_number', 'goods_description', 'ref', 'delivery_distance', 'amount']

        extra_kwargs = {
                    'ref': {'required': False}
        }

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        models = Notification
        fields = '__all__'

class AcceptDeliveryRequestSerializer(serializers.Serializer):
    delivery_id = serializers.IntegerField()


    def save(self, rider):
        delivery_id = self.validated_data.get('delivery_id')
        delivery_model = get_object_or_404(Delivery, id=delivery_id)
        
        # check if  payment has been made to request
        if delivery_model.status == delivery_model.STEPS.get(1):
            raise serializers.ValidationError({'details': 'delivery payment not verified'})
            
        return delivery_model.accept_request(rider)
         
