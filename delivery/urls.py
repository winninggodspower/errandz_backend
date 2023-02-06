from django.urls import path
from .views import DeliveryView, NotificationView, AcceptDeliveryRequestView, SuccessfulDeliveryView

urlpatterns = [
    path('make_delivery', DeliveryView.as_view()),
    path('get_notification', NotificationView.as_view()),
    path('accept_delivery_request', AcceptDeliveryRequestView.as_view()),
    path('successful_delivery', SuccessfulDeliveryView.as_view()),
]
