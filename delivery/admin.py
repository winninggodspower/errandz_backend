from django.contrib import admin
from .models import Notification, History, Delivery

# Register your models here.

admin.site.register(Notification)
admin.site.register(Delivery)
admin.site.register(History)