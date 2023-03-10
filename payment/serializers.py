from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import RiderPickupEarning, AccountDetail, RiderPayment
from user_auth.models import Rider

class RiderPickupEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderPickupEarning
        exclude = ['rider']


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetail
        fields = ['account_number', 'bank_name', 'bank_code', 'account_name' ]
        # exclude = ['rider', 'is_account_valid', 'recipient_code']
        read_only_fields = ["account_name"]

    
    def validate(self, data):
        is_account_detail_valid, result = AccountDetail.resolve_account_detail(
            bank_code=data.get('bank_code'),
            account_number=data.get('account_number'),
        )

        if not is_account_detail_valid:
            raise serializers.ValidationError(result)
        
        return data
    
class RiderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderPayment
        fields = ["amount", "transfer_ref"]
        read_only_fields = ["transfer_ref"]

    def validate(self, data):
        rider = self.context.get('rider')
        if data.get("amount") > rider.get_unpaid_balance():
            raise serializers.ValidationError("amount specified greater than earning ")
        
        return data
    
    def save(self, **kwargs):
        payment = RiderPayment(
            amount = self.validated_data['amount'],
            **kwargs
        )
        
        status, result = payment.make_payment()
        if not status:
            raise serializers.ValidationError(result)
        
        
