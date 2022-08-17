from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView 
from django.conf import settings 
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.serializers import UserSerializer
from rest_framework.views import APIView
# Create your views here.


User = settings.AUTH_USER_MODEL


class GetCustomerList(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes=[IsAdminUser]

class GetCustomerDetails(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset=User.objects.all()
    permission_classes = [IsAdminUser]

class AddProductAPI(APIView):
    pass


class EditProductAPI(UpdateAPIView):
    pass

class DeleteProductAPI()
