from django.urls import path
from account.views import RegisterApiView,LoginApiView,AuthUserApiView

urlpatterns=[
    path('register/',RegisterApiView.as_view(),name='register'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('user/', AuthUserApiView.as_view(), name='user-account')
]