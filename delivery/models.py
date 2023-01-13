from django.db import models
from user_auth.models import Customer, Rider

# Create your models here.

class Delivery(models.Model):
    customer                = models.ForeignKey(Customer, on_delete=models.CASCADE)
    pickup_location         = models.CharField( max_length=50)
    recipient_name          = models.CharField( max_length=50)
    recipient_email         = models.EmailField( max_length=254)
    recipient_phone_number  = models.CharField( max_length=50)
    pickup_date             = models.DateTimeField(auto_now_add=True)

    delivery_date           = models.DateTimeField(null=True)
    delivery_location       = models.CharField(max_length=50)
    recievers_name          = models.CharField(max_length=50)
    receivers_email         = models.EmailField( max_length=254)
    receiver_phone_number   = models.CharField(max_length=11)
    goods_description       = models.TextField()

    has_driver_accepted_request = models.BooleanField(default=False)
    accepted_rider              = models.ForeignKey(Rider, on_delete=models.CASCADE, null=True, blank=True) 
    goods_delivered             = models.BooleanField(default=False)
    delivery_distance           = models.IntegerField()
    payment_ifo            = models.ForeignKey("PaymentInfo", on_delete=models.DO_NOTHING)

    PRICE_FOR_3KM = 500
    PRICE_FOR_1KM_ADDITION = 100

    def accept_request(self, rider: Rider):
        if self.has_driver_accepted_request == True:
            return 
        self.accepted_rider = rider
        return self.save()

    def get_delivery_amount(self):
        if self.delivery_distance <= 3:
            return self.PRICE_FOR_3KM  
        else:
            return self.PRICE_FOR_3KM + (self.delivery_distance - 3)*self.PRICE_FOR_1KM_ADDITION

class PaymentInfo(models.Model):
    amount = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)

