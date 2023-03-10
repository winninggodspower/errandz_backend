from django.urls import path
from .views import registerDeviceNotificationTokenView

urlpatterns = [
    path("register_user_device_notification_token", registerDeviceNotificationTokenView)
]