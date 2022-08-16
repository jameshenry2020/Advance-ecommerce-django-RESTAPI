
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from products.models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from products.serializers import ProductDetailSerializer, ProductSerializer, OrderSerializer,AddressSerializer, TransactionSerializer, CompletedOrderSerializer
from datetime import datetime
import string
import random
# Create your views here.

stripe.api_key =settings.STRIPE_SECRET_KEY



def generate_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

current_time=datetime.now()

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


class AddDeliveryAddressView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=AddressSerializer(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        


class CheckUserAlreadyHasAddress(APIView):
    def get(self, request, *args, **kwargs):
        address_qs=ShippingAddress.objects.filter(user=request.user, default_add=True)
        if address_qs.exists():
            addr=address_qs[0]
            return Response({'HasDefaultAddress': True, 'address':addr.address}, status=status.HTTP_200_OK)
        return Response({'HasDefaultAddress': False}, status=status.HTTP_200_OK) 


class UseDefaultAddressView(APIView):
    def get(self, request, *args, **kwargs):
        address=ShippingAddress.objects.get(user=request.user, default_add=True)
        new_order_qs=Order.objects.filter(user=request.user, isPaid=False)
        if new_order_qs.exists():
            new_order=new_order_qs[0]
            new_order.shippingAd=address
            new_order.shippingFee=20.0
            new_order.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'message':'you do not have any active order'}, status=status.HTTP_400_BAD_REQUEST)

    

class GetDeliveryAddress(RetrieveAPIView):
    serializer_class=AddressSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        try:
            address=ShippingAddress.objects.get(user=self.request.user, orders__isPaid=False)
            return address
        except ObjectDoesNotExist as e:
            return None

class GetDefaultAddress(RetrieveAPIView):
    serializer_class=AddressSerializer
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        try:
            address=ShippingAddress.objects.get(user=self.request.user, default_add=True)
            return address
        except ObjectDoesNotExist as e:
            return None

class CheckCustomerCardAreadyExists(APIView):
    def get(self, request, *args, **kwargs):
        transactions=TransactionHistory.objects.filter(user=request.user)
        if transactions.exists():
            trans=transactions[0]
            if trans.stripe_customer_id is not None:
                customer_payment = stripe.Customer.list_payment_methods(
                trans.stripe_customer_id,
                type="card"
                )
                payment=customer_payment.data[0]
                card_detail=payment.card
                return Response({'data':card_detail,'hasCard':True}, status=status.HTTP_200_OK)
        return Response({'hasCard':False}, status=status.HTTP_200_OK)
        
                
            


#api endpoint to use customer saved card for current payment
class UseCustomerPreviousCard(APIView):
    def post(self, request, *args, **kwargs):
        order=Order.objects.get(user=request.user, isPaid=False)
        amt=int(order.get_total()) * 100
        user=request.user
        history=TransactionHistory.objects.filter(user=user)
        if history.exists():
            customer=history[0]
            payment_methods = stripe.PaymentMethod.list(
            customer=customer.stripe_customer_id,
            type='card'
                 )
            payment_intent = stripe.PaymentIntent.create(
            amount=amt,
            currency='usd',
            customer=customer.stripe_customer_id,
            payment_method=payment_methods.data[0].id,
            off_session=True,
            confirm=True,
            metadata={
                       'customer_email':user.email,           
                    },
           )
            if payment_intent.status == 'succeeded':
                return Response({'message':' payment Successfully', 'payment_intent_status':payment_intent.status}, status=status.HTTP_200_OK)
        
        return Response({'message':'this card is invalid please enter a new card'}, status=status.HTTP_403_FORBIDDEN)





class StripeIntentView(APIView):
    def post(self, request, *args, **kwargs):
        user=request.user
        name=f"{user.first_name} {user.last_name}"
        #save payment detail for reused by customer
        saved_card=self.request.data['save_card']
        if saved_card is True:
            customer = stripe.Customer.create(name=name,email=user.email, phone=user.phone)
            try:
                order_qs=Order.objects.filter(user=user, isPaid=False)
                if order_qs.exists():
                    order=order_qs[0]
                    amt=order.get_total()   
                    intent = stripe.PaymentIntent.create(
                        customer=customer['id'],
                        setup_future_usage='off_session',
                        amount=int(amt) * 100,
                        currency=request.data.get('currency', 'usd'),
                        automatic_payment_methods={
                            'enabled': True,
                        },
                        metadata={
                            'customer_email':user.email,
                            'saved_card':True
                        },
                    )
                    return Response({
                        'clientSecret': intent['client_secret']
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:      
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                order_qs=Order.objects.filter(user=user, isPaid=False)
                if order_qs.exists():
                    order=order_qs[0]
                    amt=order.get_total()   
                    intent = stripe.PaymentIntent.create(
                        amount=int(amt) * 100,
                        currency=request.data.get('currency', 'usd'),
                        automatic_payment_methods={
                            'enabled': True,
                        },
                        metadata={
                            'customer_email':user.email,
                            'saved_card':False
                        },
                    )
                    return Response({
                        'clientSecret': intent['client_secret']
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:      
                return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt

def stripe_webhook_view(request): 
    endpoint_secret='whsec_231dbbe88ddce282857f9b713195ff914e5b6f91e35225e9f1640ea34952b6c2'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    if endpoint_secret:
        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if event and event['type']=='payment_intent.succeeded':

        intent = event['data']['object']
        print(intent)
        intent_reponse=intent['charges']['data'][0]
        customer_email=intent_reponse['metadata']['customer_email']
        amount=intent['amount']
        user=CustomUser.objects.get(email=customer_email)
        order=Order.objects.get(user=user, isPaid=False)
        #create a transaction history
        history=TransactionHistory.objects.create(
             stripe_customer_id=intent_reponse['customer'] or None,
             amount=int(amount)/100,
             user=user,
             status='success'


         )
        order_items=order.items.all()
        order_items.update(completed=True)
        for item in order_items:
            item.save()
            #update the order
        order.isPaid=True
        order.payment=history
        order.reference_code=generate_ref_code()
        order.paidAt=current_time
        order.save()
                    
    elif event['type'] == 'payment_method.attached':
        payment_method = event['data']['object']  # contains a stripe.PaymentMethod
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)
    else:
            # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))
        return Response({'message':'Unhandled event type'}, status.HTTP_400_BAD_REQUEST)

    return HttpResponse({'success':True}, status=status.HTTP_200_OK)    #sending confimation mail
    

class getTransactionHistory(ListAPIView):
    serializer_class=TransactionSerializer 
    permission_classes=[IsAuthenticated] 

    def get_queryset(self):
        return TransactionHistory.objects.filter(user=self.request.user)


class getCompletedOrders(ListAPIView):
    serializer_class=CompletedOrderSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        orders=Order.objects.filter(user=self.request.user, isPaid=True)
        if orders.exists():
            return orders
        return None

class getCompletedOrderDetail(RetrieveAPIView):
    serializer_class=CompletedOrderSerializer
    permission_classes=[IsAuthenticated]

    def get_object(self):
        try:
            order=Order.objects.get(user=self.request.user, isPaid=True)
            return order
        except ObjectDoesNotExist:
            return Response({'message':'you do not have any order yet'}, status=status.HTTP_204_NO_CONTENT)
        