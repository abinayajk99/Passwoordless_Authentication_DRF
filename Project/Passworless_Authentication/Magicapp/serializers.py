from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import EmailRegister
from django.contrib.auth.models import User 
from drfpasswordless.models import CallbackToken



class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    token = serializers.CharField(max_length=200, required=True)


    def validate(self, data):
        try:
            CallbackToken.objects.get(to_alias=data['email'],key=data['token'],is_active=True)
        except:
            raise serializers.ValidationError("Email and token not match with each other or token not validate ")
        return data