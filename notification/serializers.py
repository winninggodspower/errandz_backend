from rest_framework import serializers


class registerDeviceNotificationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


    def save(self, **kwargs):
        # getting account from kwargs
        account = {**kwargs}.get("account")

        # raise error if account is not passed
        assert not account, "account needed to be passed to serializer the saved method"

        # updating user authentication token
        account.notification_token = self.validated_data['token']



