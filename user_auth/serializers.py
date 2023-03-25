from rest_framework import serializers
from user_auth.models import Account, Rider, Customer, Vendor
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.sites.models import Site


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
        print('%s/%s' % (Site.objects.get_current().domain, obj.profile_image))
        return '%s/%s' % (Site.objects.get_current().domain, obj.profile_image)

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

        if Account.objects.filter(phone=account.phone).all():
            raise serializers.ValidationError(
                {'phone': 'account with this phone already exist'})

        account.set_password(password)
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):
    phone = PhoneNumberField(region="NG")
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Account
        fields = ['id', 'email', 'phone', 'state',
                  'city', 'user_type', 'profile_image', 'image_url']

        extra_kwargs = {
            'user_type': {'required': True},
        }

    def get_image_url(self, obj):
        return 'https://%s/%s' % (Site.objects.get_current().domain, obj.profile_image)

    def validate_email(self, value):
        user = self.context['user']
        if Account.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use"})
        return value

    def validate_phone(self, value):
        user = self.context['request'].user
        if Account.objects.exclude(pk=user.pk).filter(phone=value).exists():
            raise serializers.ValidationError(
                {"username": "This phone number is already in use."})
        return value

    def update(self, instance, validated_data):

        instance.email = validated_data.get(
            'email') if validated_data.get('email') else instance.email
        instance.phone = validated_data.get(
            'phone') if validated_data.get('phone') else instance.phone
        instance.state = validated_data.get(
            'state') if validated_data.get('state') else instance.state
        instance.city = validated_data.get(
            'city') if validated_data.get('city') else instance.city
        instance.profile_image = validated_data.get(
            'profile_image') if validated_data.get('profile_image') else instance.profile_image

        instance.save()

        return instance


class RiderRegisterSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Rider
        fields = ['first_name', 'last_name', 'account']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account_data['user_type'] = 'rider'
        account = AccountRegistrationSerializer(
            data=account_data)
        account.is_valid()
        account = account.save()
        rider = Rider.objects.create(**validated_data, account=account)
        return rider

    def update(self, instance, validated_data):
        request = self.context['request']
        user_type_model = request.user.user_type

        if validated_data.get('account'):
            account_data = validated_data.pop('account')
            account = AccountSerializer(
                request.user, data=account_data, partial=True, context={'request': request})

            account.is_valid(raise_exception=True)
            account = account.save()

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        instance.save()
        return instance


class CustomerRegisterSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'account']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account_data['user_type'] = 'customer'
        account = AccountRegistrationSerializer(data=account_data)
        account.is_valid()
        account = account.save()
        customer = Customer.objects.create(**validated_data, account=account)
        return customer

    def update(self, instance, validated_data):
        request = self.context['request']
        user_type_model = request.user.user_type

        if validated_data.get('account'):
            account_data = validated_data.pop('account')
            account = AccountSerializer(
                request.user, data=account_data, partial=True, context={'request': request})

            account.is_valid(raise_exception=True)
            account = account.save()

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        instance.save()
        return instance


class VendorRegisterSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = Vendor
        fields = ['company_name', 'company_address', 'account']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        account_data['user_type'] = 'vendor'
        account = AccountRegistrationSerializer(data=account_data)
        account.is_valid()
        account = account.save()
        customer = Vendor.objects.create(**validated_data, account=account)
        return customer

    def update(self, instance, validated_data):
        request = self.context['request']
        user_type_model = request.user.user_type

        if validated_data.get('account'):
            account_data = validated_data.pop('account')
            account = AccountSerializer(
                request.user, data=account_data, partial=True, context={'request': request})

            account.is_valid(raise_exception=True)
            account = account.save()

        print(validated_data)
        instance.company_name = validated_data['company_name']
        instance.company_address = validated_data['company_address']

        instance.save()
        return instance
