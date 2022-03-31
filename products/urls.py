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
    path('remove-from-cart/', OrderItemQuantityUpdateView.as_view(), name='remove-from-cart')
]