from django.db import models
from . import receivers
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# create a new user
# create a superuser

class MyAccountManager(BaseUserManager):

    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_profile_image_path(self, filename):
    return f'profile_images/{self.pk}/profile_image.png'

def get_default_profile_image():
    return 'profile_images/default/profile_avatar.png'

ACCOUNT_CHOICES = (
    ('rider', 'Rider'),
    ('vendor', 'Vendor'),
    ('customer', 'Customer'),
)
    

class Rider(models.Model):
    first_name          = models.CharField(max_length=30)
    last_name           = models.CharField(max_length=30)
    account             = models.OneToOneField('Account', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Vendor(models.Model):
    company_name        = models.CharField( max_length=50, unique=True)
    company_address     = models.CharField( max_length=50, unique=True)
    account             = models.OneToOneField('Account', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.company_name

class Customer(models.Model):
    first_name          = models.CharField(max_length=30)
    last_name           = models.CharField(max_length=30)
    account             = models.OneToOneField('Account', on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    


class Address(models.Model):
    state               = models.CharField(max_length=30)
    city                = models.CharField(max_length=30)



# Create your models here.
class Account(AbstractBaseUser):
    email               = models.EmailField(verbose_name='email', max_length=60, unique=True)
    phone               = models.CharField(max_length=11, unique=True)
    date_joined         = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login          = models.DateField(verbose_name='last login', auto_now=True)
    is_admin            = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    profile_image       = models.ImageField(max_length=255, upload_to=get_profile_image_path, null=True, blank=True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=False)

    state               = models.CharField(max_length=30)
    city                = models.CharField(max_length=30)
    user_type           = models.CharField(choices=ACCOUNT_CHOICES, max_length=20)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self) -> str:
        return self.email

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    ACCOUNT_TYPE_MODEL = {
        'rider': Rider,
        'customer': Customer,
        'vendor': Vendor
    }

    def get_account_type_instance(self):
        return self.ACCOUNT_TYPE_MODEL.get(self.user_type).objects.get(account=self)
        

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


class Address(models.Model):
    state               = models.CharField(max_length=30)
    city                = models.CharField(max_length=30)
