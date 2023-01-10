from rest_framework import serializers
from .models import Account, Rider, Customer, Vendor


class AccountRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
      model = Account
      fields = ['email', 'phone', 'state', 'city', 'password', 'password2', 'user_type']
      extra_kwargs = {
        'password': {'write_only': True},
      }

    def save(self):
        account = Account(
          email = self.validated_data['email'],
          phone = self.validated_data['phone'],
          state = self.validated_data['state'],
          city = self.validated_data['city'],
          user_type = self.validated_data['user_type']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
          raise serializers.ValidationError({'password2': 'Passwords must match'})

        account.set_password(password)
        account.save()
        return account


class RiderRegisterSerializer(serializers.ModelSerializer):
      account = AccountRegistrationSerializer()
      class Meta:
        model = Rider
        fields = ['first_name', 'last_name', 'account']

      def create(self, validated_data):
        account_data = validated_data.pop('account')
        account_data['user_type'] = 'rider'
        print(account_data)
        account = AccountRegistrationSerializer(data=account_data)
        account.is_valid()
        account = account.save()
        rider = Rider.objects.create(**validated_data, account=account)
        return rider

class CustomerRegisterSerializer(serializers.ModelSerializer):
  account = AccountRegistrationSerializer()
  class Meta:
    model = Customer
    fields = ['first_name', 'last_name', 'account']

  def create(self, validated_data):
    account_data = validated_data.pop('account')
    account_data['user_type'] = 'customer'
    print(account_data)
    account = AccountRegistrationSerializer(data=account_data)
    account.is_valid()
    account = account.save()
    customer = Customer.objects.create(**validated_data, account=account)
    return customer
  
class VendorRegisterSerializer(serializers.ModelSerializer):
  account = AccountRegistrationSerializer()
  class Meta:
    model = Vendor
    fields = ['company_name', 'company_address', 'account']

  def create(self, validated_data):
    account_data = validated_data.pop('account')
    account_data['user_type'] = 'vendor'
    print(account_data)
    account = AccountRegistrationSerializer(data=account_data)
    account.is_valid()
    account = account.save()
    customer = Vendor.objects.create(**validated_data, account=account)
    return customer