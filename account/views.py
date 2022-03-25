from account.models import CustomUser
from account.serializers import UserSerializer, UserSerilaizerWithToken, PasswordResetRequestSerializer, NewPasswordSetSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, GenericAPIView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str,force_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class MyTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)

        serializer=UserSerilaizerWithToken(self.user).data
        for k, v in serializer.items():
            data[k]=v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer



class UserSignUpView(GenericAPIView):
    serializer_class=UserSerilaizerWithToken
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserProfile(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user=request.user
        serializer=UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)




class GetAllCustomerUser(ListAPIView):
    permission_classes=[IsAdminUser]
    serializer_class=UserSerializer
    queryset=CustomUser.objects.all()
    

class RequestPasswordReset(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'a link to reset your password has been sent to your email!'})
        return Response({'error':'invalid credentials'})



class PasswordResetTokenCheckView(GenericAPIView):
    def get(self, request, uidb64, token, **kwargs):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success':True, 'message':'credential valid', 'uidb64':uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as e:
            return Response({'error':'token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        
class PasswordResetCompleteApiView(GenericAPIView):
    serializer_class=NewPasswordSetSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password Reset Successfully'})