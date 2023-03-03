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
    account_type        = models.CharField(choices=(('personal', 'personal'),( 'business' , 'business' )), max_length=100, null=True, blank=True)
    country_code        = models.CharField(default="NG", max_length=2)
    bank_code           = models.CharField(max_length=15)
    bank_name           = models.CharField(max_length=200, null=True, blank=True)
    document_type       = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES, null=True, blank=True)
    document_number     = models.CharField(max_length=100, null=True, blank=True)

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
    
    @classmethod
    def resolve_account_detail(cls, account_number=None, bank_code=None):
        paystack = PayStack()
        bank_code = bank_code or cls.bank_code
        account_number = account_number or cls.account_number

        status, result = paystack.resolve_account_detail(account_number, bank_code)

        return status, result

    def generate_recipient_code(self, **kwargs):
        paystack = PayStack()
        status, result = paystack.generate_transfer_recipient(**kwargs)
        print("this is the result: ", result)
        if status:
            self.recipient_code = result.get("recipient_code")
            self.bank_name = result.get("details").get("bank_name")
            print(result.get("details").get("bank_name"))
            self.save()

    def save(self, *args, **kwargs):
        is_account_detail_valid, result = self.resolve_account_detail(self.account_number, self.bank_code)
        if is_account_detail_valid:
            self.account_name = result.get('account_name')
        return super().save(*args, **kwargs)
    
    def delete_recipient(self):
        self.recipient_code = None
        self.save()
        print(self.recipient_code)


class RiderPayment(models.Model):
    transfer_ref   = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)
    amount         = models.IntegerField()
    rider           = models.ForeignKey("user_auth.Rider", on_delete=models.CASCADE)
    payment_successful = models.BooleanField(default=False)

    def make_payment(self):
        paystack = PayStack()
        if self.rider.get_unpaid_balance >= self.amount and self.rider.get_account_detail.recipient_code: 
            status, result = paystack.validate_account(
                                type="nuban",
                                name=self.account_name,
                                bank_code=self.bank_code,
                                account_number=self.account_name, 
                                currency="NGN"
                                )

class RiderPickupEarning(models.Model):
    amount          = models.IntegerField(default=100)
    date_created    = models.DateTimeField( auto_now_add=True)
    delivery_model  = models.OneToOneField("delivery.Delivery", on_delete=models.DO_NOTHING)
    rider           = models.ForeignKey("user_auth.Rider", on_delete=models.CASCADE)
