from django.urls import path
from .views import DeliveryView, NotificationView, AcceptDeliveryRequestView, SuccessfulDeliveryView, GetDeliveryView,ConfirmDelivery

urlpatterns = [
    path('make_delivery', DeliveryView.as_view()),
    path('get_notification', NotificationView.as_view()),
    path('accept_delivery_request', AcceptDeliveryRequestView.as_view()),
    path('successful_delivery', SuccessfulDeliveryView.as_view()),
    path('get_delivery_details/<uuid:pk>', GetDeliveryView.as_view()),
    path("confirm_delivery",ConfirmDelivery.as_view()),
]
