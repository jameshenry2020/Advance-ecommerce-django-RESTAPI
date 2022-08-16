from unicodedata import name
from django.urls import path
from products.views import *


urlpatterns=[
    path('products/', AllProductListView.as_view(), name='products'),
    path('top-products/', TopProductListView.as_view(), name='top-product'),
    path('latest-products/', LatestProductListView.as_view(), name='latest-products'),
    path('products/<pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('fetch-order-summary/', OrderDetailView.as_view(), name='order-summary'),
    path('order-item/<pk>/delete', OrderItemDeleteView.as_view(), name='order-item-delete'),
    path('remove-from-cart/', OrderItemQuantityUpdateView.as_view(), name='remove-from-cart'),
    path('add-delivery-address/', AddDeliveryAddressView.as_view(), name='delivery-address'),
    path('get-default-address/', GetDefaultAddress.as_view(), name='get-saved-address'),
    path('has-default-address/', CheckUserAlreadyHasAddress.as_view(), name='default-address'),
    path('use-default-address/', UseDefaultAddressView.as_view(), name='use-default'),
    path('create-payment-intent/', StripeIntentView.as_view(), name='create-stripe-intent'),
    path('check-user-saved/', CheckCustomerCardAreadyExists.as_view(), name='saved-card'),
    path('transaction-history/', getTransactionHistory.as_view(), name='payment-history'),
    path('fetch-completed-orders/', getCompletedOrders.as_view(), name='orders-list'),
    path('retrieve-address/', GetDeliveryAddress.as_view(), name='retrieve-address'),
    path('pay-with-default-card/', UseCustomerPreviousCard.as_view(), name='payment-with-default-card'),
    path('payment-webhook/', stripe_webhook_view, name='webhook')
]