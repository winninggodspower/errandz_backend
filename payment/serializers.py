from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import RiderPickupEarning, AccountDetail

class RiderPickupEarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderPickupEarning
        exclude = ['rider']


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountDetail
        # fields = '__all__'
        exclude = ['rider', 'is_account_valid', 'recipient_code']
        # read_only_fields = ['rider']

    
    def validate(self, data):
        is_valid_account_details, result = AccountDetail.validate_account(
            bank_code=data.get('bank_code'),
            country_code=data.get('country_code'),
            account_number=data.get('account_number'),
            account_type=data.get('account_type'),
            account_name=data.get('account_name'),
            document_type=data.get('document_type'),
            document_number=data.get('document_number'),
        )

        if not is_valid_account_details:
            raise serializers.ValidationError(result)
        
        return data