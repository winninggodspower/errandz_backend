from rest_framework import serializers
from user_auth.models import Account, Rider, Customer, Vendor
from phonenumber_field.serializerfields import PhoneNumberField


class AccountRegistrationSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region="NG")
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Account
        fields = ['id', 'email', 'phone', 'state',
                  'city', 'password', 'password2', 'user_type', 'profile_image', 'image_url']
        extra_kwargs = {
            'password': {'write_only': True},
            'user_type': {'required': False}
        }

    def get_image_url(self, obj):
        request = self.context.get("request")
        print(self.context)
        return request.build_absolute_uri(obj.profile_image.url)

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            state=self.validated_data['state'],
            city=self.validated_data['city'],
            user_type=self.validated_data['user_type']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'password2': 'Passwords must match'})

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


class AccountSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'email', 'phone', 'state',
                  'city', 'user_type', 'profile_image']

        extra_kwargs = {
            'user_type': {'required': True},
        }

    def get_profile_image(self, obj):
        request = self.context.get("request")
        print('this method is called')
        return obj.profile_image.url
