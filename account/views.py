from django.shortcuts import get_object_or_404, render
from rest_framework.generics import GenericAPIView
from account.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import authenticate
from account.jwt import JWTAuthentication
# Create your views here.


class AuthUserApiView(GenericAPIView):
    serializer_class=UserSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):
        user=request.user
        serializer=self.serializer_class(user)
        return Response({'user':serializer.data})



class RegisterApiView(GenericAPIView):
    permission_classes=[permissions.AllowAny]
    serializer_class=RegisterSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class=LoginSerializer
    permission_classes=[permissions.AllowAny]
    def post(self, request):
        email=request.data.get('email', None)
        password=request.data.get('password',None)

        user=authenticate(username=email, password=password)

        if user:
            serializer=self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'invalid credentials try again'}, status=status.HTTP_400_BAD_REQUEST)

