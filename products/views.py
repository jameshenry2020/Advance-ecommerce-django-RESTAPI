from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from products.models import *
from rest_framework.permissions import AllowAny
from products.serializers import ProductDetailSerializer, ProductSerializer
# Create your views here.



class AllProductListView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]
    

class TopProductListView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        result=self.queryset.filter(rating__gte=4).order_by('-rating')[0:8]
        return result


class LatestProductListView(ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[AllowAny]

    def get_queryset(self):
        result=self.queryset.filter(category='hoodies').order_by('-created_at')[0:6]
        return result

class ProductDetailView(RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductDetailSerializer
    queryset=Product.objects.all()
