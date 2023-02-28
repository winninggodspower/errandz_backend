from django.db import models
from user_auth.models import Customer, Rider, Account
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import get_object_or_404
import uuid
from .Paystack import PayStack
from payment.models import RiderPickupEarning

# Create your models here.

class Delivery(models.Model):
    STEPS = {
        1: 'payment not verified',
        2: 'rider\'s not yet accepted request',
        3: 'pending delivery',
        4: 'completed'
    }

    ref                     = models.UUIDField(
                                            default = uuid.uuid4,
                                            editable = False,
                                            primary_key=True,
                                            unique=True)
    customer                = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pickup_location         = models.CharField( max_length=500)
    recipient_name          = models.CharField( max_length=500)
    recipient_email         = models.EmailField( max_length=254)
    recipient_phone_number  = PhoneNumberField()
    pickup_date             = models.DateTimeField(auto_now_add=True)

    delivery_location       = models.CharField(max_length=500)
    recievers_name          = models.CharField(max_length=500)
    receivers_email         = models.EmailField( max_length=254)
    receiver_phone_number   = PhoneNumberField()
    goods_description       = models.TextField()

    has_driver_accepted_request = models.BooleanField(default=False)
    rider_who_accepted          = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True) 
    goods_delivered             = models.BooleanField(default=False)
    delivery_distance           = models.PositiveIntegerField()
    notification_sent           = models.BooleanField(default=False)

    amount                  = models.PositiveIntegerField(null=True, blank=True)
    checkout_url            = models.CharField( max_length=500, null=True, blank=True)
    payment_verified        = models.BooleanField(default=False)
    date_created            = models.DateTimeField(auto_now_add=True)
    last_updated            = models.DateTimeField(auto_now=True)

    status                  = models.CharField(max_length=100, default=STEPS.get(1)) 

    class Meta:
        ordering = ('-date_created',)

    PRICE_FOR_3KM = 600
    PRICE_FOR_1KM_ADDITION = 100


    def accept_request(self, account: Account):
        if not account.user_type == 'rider':
            return

        if self.has_driver_accepted_request == True:
            return 
        self.rider_who_accepted = account.get_account_type_instance()
        self.has_driver_accepted_request = True
        self.status = self.STEPS.get(3)
        return self.save()

    def get_delivery_amount(self):
        if self.delivery_distance <= 3:
            return self.PRICE_FOR_3KM
        else:
            return self.PRICE_FOR_3KM + (self.delivery_distance - 3)*self.PRICE_FOR_1KM_ADDITION

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        
        if status:
            # if result['amount'] / 100 == self.amount and self.amount == self.get_delivery_amount():
            self.payment_verified = True
            self.status = self.STEPS.get(2)
            self.save()
        
        return self.payment_verified
    
    def confirm_delivery(self, ref):
        delivery_model = get_object_or_404(Delivery, pk=ref)
        
        # checking if the delivery_status is pending delivery
        if delivery_model.status != delivery_model.STEPS.get(3):
            return False

        delivery_model.goods_delivered = True
        delivery_model.status = delivery_model.STEPS.get(4)
        delivery_model.save()

        # add earning for rider
        RiderPickupEarning.objects.create(
            delivery_model = self,
            rider          = self.rider_who_accepted
        )

        for account in [delivery_model.customer, delivery_model.rider_who_accepted]:
            Notification.objects.create(
                message = f"{delivery_model.recievers_name} received her/his goods",
                type = Notification.TYPE[1],
                account = account.account
            )
        return True



    def get_uuid_string(self):
        return str(self.ref)

    def save(self, *args, **kwargs):
        self.amount = self.get_delivery_amount()
        super(Delivery, self).save(*args, **kwargs)

class Notification(models.Model):
    TYPE = [
        ('request', "request"),
        ('received', "received")
    ]

    message = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    model   = models.ForeignKey(Delivery, blank=True, null=True, on_delete=models.CASCADE)
    type    = models.CharField( max_length=50, choices=TYPE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    seen    = models.BooleanField(default=False)

class History(models.Model):
    message = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)