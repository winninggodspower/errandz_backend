from .views import RiderEarningView, get_bank_list, AccountDetailView
from django.urls import path

urlpatterns = [
    path('get_rider_earning', RiderEarningView.as_view()),
    path('get_bank_list', get_bank_list),
    path('add_account_details', AccountDetailView.as_view()),
]
