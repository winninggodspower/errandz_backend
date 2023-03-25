from django.urls import path
from .views import registerDeviceNotificationTokenView, get_notification

urlpatterns = [
    path("register_user_device_notification_token", registerDeviceNotificationTokenView),
    path("send_demo_notification", get_notification),
]