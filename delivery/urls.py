from django.urls import path
from .views import DeliveryView

urlpatterns = [
    path('make_delivery', DeliveryView.as_view())
]
