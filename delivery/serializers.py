from django.shortcuts import get_object_or_404
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Delivery, Notification, History

class DeliverySerializer(serializers.ModelSerializer):
    recipient_phone_number = PhoneNumberField(region="NG")
    receiver_phone_number = PhoneNumberField(region="NG")
    class Meta:
        model = Delivery
        fields = ['ref', 'pickup_location', 'recipient_name', 'recipient_email', 'recipient_phone_number', 'delivery_location', 'recievers_name', 'receivers_email', 'receiver_phone_number', 'goods_description', 'delivery_distance', 'status','checkout_url','date_created', 'amount']

        extra_kwargs = {
                    'ref': {'read_only': True},
                    'status': {'read_only': True},
                    'checkout_url': {'read_only': True},
        }


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'


class AcceptDeliveryRequestSerializer(serializers.Serializer):
    delivery_ref = serializers.IntegerField()


    def save(self, rider):
        delivery_ref = self.validated_data.get('delivery_ref')
        delivery_model = get_object_or_404(Delivery, ref=delivery_ref)
        
        # check if  payment has been made to request
        if delivery_model.status == delivery_model.STEPS.get(1):
            raise serializers.ValidationError({'details': 'delivery payment not verified'})
        
        # setting the delivery model to step to 
        delivery_model.status = delivery_model.STEPS.get(3)
        delivery_model.save()

        return delivery_model.accept_request(rider)
         
