from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccountDetail


@receiver(post_save, sender=AccountDetail)
def generate_recipient(sender, instance, created, **kwargs):
    if not instance.recipient_code:
        instance.generate_recipient_code(
            type= "nuban", 
            name= instance.account_name,
            account_number= instance.account_number, 
            bank_code= instance.bank_code, 
            currency= "NGN"
        )