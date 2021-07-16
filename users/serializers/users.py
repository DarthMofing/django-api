""" Users Serializers """
#Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from django.contrib.auth.models import User
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    """ Prifile model serializer """
    class Meta:
        model=Profile
        fields=['age','country','city','followers','likes','posts','profile_pic','hero_badge']

class UserSerializer(serializers.ModelSerializer):
    """ User model serializer """
    profile=ProfileSerializer(read_only=True)
    
    class Meta:
        model=User
        fields=['username','first_name','last_name','profile']