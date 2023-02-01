
# code
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Delivery, Notification
from user_auth.models import Account
from django.conf import settings
from twilio.rest import Client



@receiver(post_save, sender=Delivery)
def create_profile(sender, instance, created, **kwargs):
    if created :
        # instance.verify_payment()
        if not instance.payment_verified and not instance.notification_sent:
            riders = Account.objects.filter(user_type='rider').all()

            # send the email here
            for rider in riders:
                Notification(
                    message = 'incomming delivery request',
                    account = rider
                )

            #send text to drivers
            client = Client(settings.account_sid, settings.auth_token)
            message = client.messages.create(
                     body="Incoming delivery request. check you dashboard notification to accept",
                     from_=settings.twilio_phone_number,
                     to=[rider.phone for rider in riders]
                    )


            instance.notification_sent = True