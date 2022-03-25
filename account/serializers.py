from dataclasses import field
from django.forms import ValidationError
from rest_framework import serializers
from account.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str,force_str, smart_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
from account.utils import Mailer
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    # name=serializers.SerializerMethodField(read_only=True)
    isAdmin=serializers.SerializerMethodField(read_only=True)
    class Meta:
        model=CustomUser
        fields=['id', 'email', 'first_name', 'last_name','phone', 'isAdmin']

    # def get_name(self, obj):
    #     name=f"{obj.first_name}  {obj.last_name}"

    #     return name 

    def get_isAdmin(self, obj):
        return obj.is_admin

class UserSerilaizerWithToken(UserSerializer):
    token=serializers.SerializerMethodField(read_only=True)
    password=serializers.CharField(max_length=128, min_length=5, write_only=True)
    class Meta:
        model=CustomUser
        fields=['id', 'email','phone', 'first_name', 'last_name', 'isAdmin', 'token', 'password']

    def get_token(self, obj):
        token=RefreshToken.for_user(obj)
        return str(token.access_token)

    def create(self, validated_data):
        user=CustomUser.objects.create_user(**validated_data)
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        fields=['email']


    def validate(self, attrs):
        email=attrs['email']
        qs=CustomUser.objects.filter(email=email).exists()
        if qs:
            user=CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(self.context.get('request')).domain
            relativeLink=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
            absLink='http://'+current_site + relativeLink
            email_body='hello \n Use the link below to reset your password \n'+absLink
            data={'subject':'Reset your password','email_body':email_body, 'to_email':user.email}         
            #send an email to the user
            Mailer.send_email(data)

        return super().validate(attrs)

    

class NewPasswordSetSerializer(serializers.Serializer):
    uid=serializers.CharField(min_length=1)
    token=serializers.CharField(min_length=1)
    password=serializers.CharField(min_length=1, max_length=80, write_only=True)
    retype_password=serializers.CharField(min_length=1, max_length=80, write_only=True)

    class Meta:
        fields=['uid','token', 'password', 'retype_password']

    def validate(self, attrs):
        try:
            uidb64=attrs.get('uid')
            token=attrs.get('token')
            password=attrs.get('password')
            retype_password=attrs.get('retype_password')

            id=force_str(urlsafe_base64_decode(uidb64))
            user=CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('the reset link is invalid', 401)
            if password != retype_password:
                raise ValidationError('passwords do not match')
            user.set_password(password)
            user.save()
            return user 
        except Exception as e:
            raise AuthenticationFailed('the reset link is invalid', 401)
        return super().validate(attrs)


    

   
