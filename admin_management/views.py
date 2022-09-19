from multiprocessing import context
from django.shortcuts import render
from rest_framework.generics import (ListAPIView, 
                                    RetrieveAPIView,
                                     UpdateAPIView, DestroyAPIView, GenericAPIView )
from account.models import CustomUser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.serializers import UserSerializer
from rest_framework.views import APIView
from products.models import Product, Order
from products.serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from admin_management.api.serializers import ProductCreateSerializer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from products.serializers import CompletedOrderSerializer, OrderSerializer




class GetCustomerList(ListAPIView):
    serializer_class =UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes=[IsAdminUser]

class GetCustomerDetails(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset=CustomUser.objects.all()
    permission_classes = [IsAdminUser]


class AddProductAPI(GenericAPIView):
    serializer_class= ProductCreateSerializer
    permission_classes =[IsAdminUser]
    parser_classes=[FormParser, JSONParser, MultiPartParser]
    def post(self, request, *args, **kwargs):
        my_thumbnails=[]
        thumbnail1=request.data.get('thumbnail1')
        thumbnail2=request.data.get('thumbnail2')
        thumbnail3=request.data.get('thumbnail3')
        my_thumbnails.append({'img':thumbnail1})
        my_thumbnails.append({'img':thumbnail2})
        my_thumbnails.append({'img':thumbnail3})
        data={
            'productname':request.data.get('productname'),
             'category':request.data.get('category'),
             'description':request.data.get('description'),
             'brand':request.data.get('brand'),
             'image':request.data.get('image'),
             'price':request.data.get('price'),
             'countInstock':request.data.get('countInstock'),
             'thumbnails':my_thumbnails

        }
        print(data)
        serializer=self.serializer_class(data=data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllCustomerOrders(ListAPIView):
    serializer_class=CompletedOrderSerializer
    queryset=Order.objects.all()
    permission_classes=[IsAdminUser]
    


class EditProductAPI(UpdateAPIView):
    serializer_class=ProductCreateSerializer
    queryset=Product.objects.all()
    permission_classes = [IsAdminUser]

class DeleteProductAPI(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classess=[IsAdminUser]


class AdminOrderDetailView(RetrieveAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAdminUser]
    queryset=Order.objects.all()

