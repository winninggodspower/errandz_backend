from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path('register/rider', views.RegisterRiderView.as_view()),
    path('register/customer', views.RegisterCustomerView.as_view()),
    path('register/vendor', views.RegisterVendorView.as_view()),
    path('api-token-auth/', obtain_auth_token)
]
