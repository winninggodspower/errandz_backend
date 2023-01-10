from django.contrib import admin
from .models import Account, Rider, Customer, Vendor

# Register your models here.
admin.site.register(Account)
admin.site.register(Rider)
admin.site.register(Customer)
admin.site.register(Vendor)