from unicodedata import name
from django.urls import path
from account.views import (GetUserProfile, 
                            GetAllCustomerUser,
                             UserSignUpView, 
                             RequestPasswordReset,
                             PasswordResetTokenCheckView,
                             PasswordResetCompleteApiView)

urlpatterns=[
  path('signup/', UserSignUpView.as_view(), name='register'),
  path('user/', GetUserProfile.as_view(), name='profile'),
  path('customers/', GetAllCustomerUser.as_view(), name='customers'),
  path('request-password-reset/', RequestPasswordReset.as_view(), name='request-pwd-reset'),
  path('password-reset-confirm/<uidb64>/<str:token>/', PasswordResetTokenCheckView.as_view(), name='password-reset-confirm'),
  path('password-reset-complete/', PasswordResetCompleteApiView.as_view(), name='password-reset-complete')
]