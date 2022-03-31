from itertools import product
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from products.models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from products.serializers import ProductDetailSerializer, ProductSerializer, OrderSerializer
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


class AddToCart(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        prod_id=request.data.get('prod_id', None)
        variation=request.data.get('variation', [])
        qty=request.data.get('qty', None)
    
        if prod_id is None:
            return Response({'message':'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        product=get_object_or_404(Product, pk=prod_id)
       
        min_variation_count=Variation.objects.filter(item=product).count()
        if len(variation) < min_variation_count:
            return Response({'message':'please specify the required variation'}, status=status.HTTP_204_NO_CONTENT)
        order_item_qs=OrderItem.objects.filter(product=product, user=request.user, completed=False)
        for v in variation:
            order_item_qs=order_item_qs.filter(
                Q(item_variations__exact=v)
                )
        if order_item_qs.exists():
            order_item=order_item_qs.first()
            if order_item.product.countInstock > order_item.quantity:
                order_item.quantity += 1
                order_item.save()
            order_item.quantity=order_item.product.countInstock
        else:
            order_item=OrderItem.objects.create(
                product=product,
                user=request.user,
                quantity=qty,
                completed=False
            )
            order_item.item_variations.add(*variation)
            order_item.save()
        
        order_qs=Order.objects.filter(user=request.user, isPaid=False)
        if order_qs.exists():
            order=order_qs[0]
            if not order.items.filter(product__id=order_item.id).exists():
                order.items.add(order_item)
            return Response({'message':'product added to cart'},status=status.HTTP_200_OK)
        else:
            order=Order.objects.create(
                user=request.user,
                isPaid=False
            )
            order.items.add(order_item)
            return Response({'message':'product added to cart'},status=status.HTTP_200_OK)

            
class OrderDetailView(RetrieveAPIView):
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        try:
            order=Order.objects.get(user=self.request.user, isPaid=False)
            return order
        except ObjectDoesNotExist:
            return Response({'message':'you do not have any item in cart'}, status=400)
        

class OrderItemDeleteView(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=OrderItem.objects.all()


class OrderItemQuantityUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        prod_id=request.data.get('prod_id', None)
        if prod_id is None:
            return Response({'message':'invalid item id'}, status=status.HTTP_400_BAD_REQUEST)
        item=get_object_or_404(Product, pk=prod_id)
        order_qs=Order.objects.filter(user=request.user, isPaid=False)
        if order_qs.exists():
            order=order_qs[0]
            if order.items.filter(product__id=item.id).exists():
                order_item=OrderItem.objects.filter(product=item, user=request.user, completed=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -=1
                    order_item.save()
                else:
                    order.items.remove(order_item)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'message':'this item is not in your cart'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'you do not have an active order'}, status=status.HTTP_404_NOT_FOUND)
