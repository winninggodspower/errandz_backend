
# code
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Delivery, Notification
from user_auth.models import Account


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
            instance.notification_sent = True