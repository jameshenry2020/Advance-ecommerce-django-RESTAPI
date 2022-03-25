from django.urls import path
from products.views import *


urlpatterns=[
    path('products/', AllProductListView.as_view(), name='products'),
    path('top-products/', TopProductListView.as_view(), name='top-product'),
    path('latest-products/', LatestProductListView.as_view(), name='latest-products'),
    path('products/<pk>/', ProductDetailView.as_view(), name='product-detail')
]