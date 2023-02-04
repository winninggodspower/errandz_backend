
# code
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Delivery, Notification, History
from user_auth.models import Account
from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client


@receiver(post_save, sender=Delivery)
def check_payment_verified(sender, instance, created, **kwargs):
    if created :
        instance.verify_payment()
        if instance.payment_verified and not instance.notification_sent:
            riders = Account.objects.filter(user_type='rider').all()

            # add customer history
            History.objects.create(
                message = instance.STEPS.get(2),
                account = instance.customer.account,
            )

            # send the email here
            for rider in riders:
                Notification(
                    message = 'incomming delivery request',
                    account = rider
                )

            #send text to drivers
            client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
            message = client.messages.create(
                     body="Incoming delivery request. check you dashboard notification to accept",
                     from_=settings.TWILIO_PHONE_NUMBER,
                     to=[rider.phone.as_international for rider in riders if rider.phone.national_number is not None]
                    )

            # send email notification
            subject = 'Incoming delivery'
            message = f'Incoming delivery from {instance.customer.first_name}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ rider.email for rider in riders ]
            send_mail( subject, message, email_from, recipient_list )

            instance.notification_sent = True

            if instance.status == instance.STEPS.get(1): 
                instance.status = instance.STEPS.get(2)