""" Account verification serializer """

#Django
from django.conf import settings

#Django REST framework
from rest_framework import serializers

#Model
from django.contrib.auth.models import User

#Utilities
import jwt

class AccountVerificationSerializer(serializers.Serializer):
    """ Account verification serializer """

    token = serializers.CharField()

    def validate_token(self,data):
        """ Verifies the token """

        try:
            payload = jwt.decode(data,settings.SECRET_KEY,algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({'Error':'Verification link expired'})
        except jwt.PyJWKError:
            raise serializers.ValidationError({'Error':'Invalid token'})

        if payload['type']!='email_confirmation':
            raise serializers.ValidationError({'Error':'Invalid token'})

        self.context['payload']=payload

        return data

    def save(self):
        """ Update user's verification status """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.profile.is_verified = True
        user.profile.save()
        return user
