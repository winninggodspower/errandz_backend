from rest_framework import serializers


class registerDeviceNotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def save(self, **kwargs):
        # getting account from kwargs
        account = {**kwargs}.get("account")
        print({**kwargs})

        # raise error if account is not passed
        assert account, "account needed to be passed to serializer the saved method"
        print(not account)

        # updating user authentication token
        account.notification_token = self.validated_data['token']
        account.save()
