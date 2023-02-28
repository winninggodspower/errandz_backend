from django.db import models
from delivery.Paystack import PayStack
import uuid

# Create your models here.

class AccountDetail(models.Model):
    DOCUMENT_TYPE_CHOICES = [
                            ('identityNumber', 'identityNumber'),
                            ('passportNumber', 'passportNumber'),
                            ('businessRegistrationNumber', 'businessRegistrationNumber') 
                            ]

    account_name        = models.CharField(max_length=200)
    account_number      = models.CharField(max_length=50)
    account_type        = models.CharField(choices=(('personal', 'personal'),( 'business' , 'business' )), max_length=100)
    country_code        = models.CharField(default="NG", max_length=2)
    bank_code           = models.CharField(max_length=15)
    bank_name           = models.CharField( max_length=200)
    document_type       = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES)
    document_number     = models.CharField(max_length=100)

    is_account_valid    = models.BooleanField(default=False)
    recipient_code      = models.CharField(max_length=100, null=True, blank=True)
    rider               = models.OneToOneField("user_auth.Rider", on_delete=models.CASCADE)

    @classmethod
    def validate_account(cls, bank_code=None, country_code=None, account_number=None, account_type=None, account_name=None, document_type=None, document_number=None):
        paystack = PayStack()
        bank_code = bank_code or cls.bank_code
        country_code = country_code or cls.country_code
        account_number = account_number or cls.account_number
        account_type = account_type or cls.account_type
        account_name = account_name or cls.account_name
        document_type = document_type or cls.document_type
        document_number = document_number or cls.document_number

        status, result = paystack.validate_account(
            bank_code=bank_code,
            country_code=country_code,
            account_number=account_number,
            account_type=account_type,
            account_name=account_name,
            document_type=document_type,
            document_number=document_number
        )
        return status, result

    def generate_recipient_code(self):
        paystack = PayStack()
        status, result = paystack.validate_account(type="nuban", name=self.account_name,
                                    bank_code=self.bank_code, account_number=self.account_name, 
                                    currency="NGN")
        if status:
            self.recipient_code = result.recipient
            self.save()


class RiderPayment(models.Model):
    transfer_ref   = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    amount         = models.IntegerField()
    rider           = models.ForeignKey("user_auth.Rider", on_delete=models.CASCADE)
    payment_successful = models.BooleanField(default=False)

    # def make_payment(self):
    #     paystack = PayStack()
    #     if self.rider.
    #     status, result = paystack.validate_account(type="nuban", name=self.account_name,
    #                                 bank_code=self.bank_code, account_number=self.account_name, 
    #                                 currency="NGN")

class RiderPickupEarning(models.Model):
    amount          = models.IntegerField(default=100)
    date_created    = models.DateTimeField( auto_now_add=True)
    delivery_model  = models.OneToOneField("delivery.Delivery", on_delete=models.DO_NOTHING)
    rider           = models.ForeignKey("user_auth.Rider", on_delete=models.CASCADE)
