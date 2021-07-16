""" User login serializer """

#Django
from django.contrib.auth import authenticate

#Django REST framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework import status

class UserLoginSerializer(serializers.Serializer):
    """ Handle the login request data """

    username=serializers.CharField(max_length=150)
    password=serializers.CharField(min_length=8,max_length=128)

    def validate(self, data):
        user=authenticate(username=data['username'],password=data['password'])

        if not user:
            raise serializers.ValidationError({status.HTTP_401_UNAUTHORIZED:'Invalid credentials'})

        if not user.profile.is_verified:
            raise serializers.ValidationError({'Login Error':'The account is not verified'})

        self.context['user']=user
        return data

    def create(self,data):
        """ Generate or retrieve new Token """
        token, create = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'],token.key