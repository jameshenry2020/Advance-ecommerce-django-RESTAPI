from rest_framework import serializers
from account.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['first_name','last_name','username','email','phone']




class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=128, min_length=6, write_only=True)
    class Meta:
        model=MyUser
        fields=['first_name','last_name','username','email','password','phone']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
        password=serializers.CharField(max_length=128, min_length=6, write_only=True)
        class Meta:
            model=MyUser
            fields=('email','username', 'password', 'token')
            read_only_fields=['token']