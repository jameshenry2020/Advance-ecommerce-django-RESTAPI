from django.urls import path
from .views import GetCustomerList, GetCustomerDetails



urlpatterns=[
    path('get-all-customers/', GetCustomerList.as_view(), name='customers'),
    path('get-customer-details/<pk>/', GetCustomerDetails.as_view(), name='customer-details')
    
]