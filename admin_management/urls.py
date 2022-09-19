from django.urls import path
from .views import ( GetCustomerList, GetCustomerDetails,GetAllCustomerOrders,
                    DeleteProductAPI, AddProductAPI,EditProductAPI, AdminOrderDetailView )



urlpatterns=[
    path('get-all-customers/', GetCustomerList.as_view(), name='customers'),
    path('get-customer-details/<pk>/', GetCustomerDetails.as_view(), name='customer-details'),
    path('delete-product/<pk>/', DeleteProductAPI.as_view(), name='delete-product'),
    path('create-product/', AddProductAPI.as_view(), name='add-product'),
    path('edit-product/', EditProductAPI.as_view(), name='edit-product'),
    path('get-customers-orders/', GetAllCustomerOrders.as_view(), name='get-all-customers-orders'),
    path('get-customers-order-detail/<pk>/', AdminOrderDetailView.as_view(), name='get-order-detail')
]