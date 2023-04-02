from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from . import views

urlpatterns = [
    path('register/rider/', views.RegisterRiderView.as_view()),
    path('register/customer/', views.RegisterCustomerView.as_view()),
    path('register/vendor/', views.RegisterVendorView.as_view()),
    path('account/', views.AccountDetail.as_view()),
    path('account/change_profile_image/', views.ChangeProfileImageApiView.as_view(),
         name="change_profile_image_api_view"),
    path('account/<int:pk>/', views.AccountDetailId.as_view()),
    path('api-token-auth/', obtain_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)
