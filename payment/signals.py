
# code
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AccountDetail
 
 
@receiver(post_save, sender=AccountDetail)
def create_profile(sender, account_detail, created, **kwargs):
    if created and not account_detail.recipient_code:
        account_detail.generate_recipient_code()