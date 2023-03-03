from django.contrib import admin
from .models import RiderPayment, RiderPickupEarning, AccountDetail

# Register your models here.
admin.site.register(RiderPayment)
admin.site.register(RiderPickupEarning)
admin.site.register(AccountDetail)