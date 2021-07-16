""" User signup serializer """

#Django
from django.contrib.auth import password_validation
from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

#Django REST framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

#Models
from django.contrib.auth.models import User
from users.models import Profile

#Utilities
import jwt
from datetime import timedelta

class UserSignupSerializer(serializers.Serializer):
    """ Handle signup data validation and user/profile creation """
    username=serializers.CharField(min_length=4,max_length=150,allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all())])
    email=serializers.EmailField(max_length=150,allow_blank=False,validators=[UniqueValidator(queryset=User.objects.all())])
    password=serializers.CharField(min_length=8,max_length=128,allow_blank=False)
    password_confirmation=serializers.CharField(min_length=8,max_length=128,allow_blank=False)
    profile_pic = serializers.ImageField()
    hero_badge = serializers.ImageField()
    first_name=serializers.CharField(max_length=150,allow_blank=False)
    last_name=serializers.CharField(max_length=150,allow_blank=False)
    city=serializers.CharField(max_length=100,allow_blank=False)
    country=serializers.CharField(max_length=100,allow_blank=False)
    age=serializers.IntegerField()
    likes=serializers.IntegerField()
    followers=serializers.IntegerField()
    posts=serializers.IntegerField()

    def validate(self,data):
        """ Verifies that passwords match and they aren't too common """
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError({'Error':"Password doesn't match with the password confirmation"})
        
        password_validation.validate_password(passwd)

        return data

    def create(self,data):
        """ Handle user and profile creation """
        data.pop('password_confirmation')

        user = User.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
        )

        profile = Profile(user=user)
        profile.profile_pic=data['profile_pic']
        profile.hero_badge=data['hero_badge']
        profile.city=data['city']
        profile.country=data['country']
        profile.age=data['age']
        profile.likes=data['likes']
        profile.followers=data['followers']
        profile.posts=data['posts']
        profile.is_verified=False

        profile.save()

        self.send_confirmation_email(user)

        return user

    def send_confirmation_email(self,user):
        """ Sends an account verification link """
        verification_token = self.gen_verification_token(user)
        subject = f'Welcome @{user.username}! Verify your account to start using this App'
        from_email = 'Application <noreply@app-com>'
        content = render_to_string(
            'emails/account_verification.html',
            {'token':verification_token,'user':user}
        )
        msg = EmailMultiAlternatives(
            subject,content,from_email,[user.email]
        )
        msg.attach_alternative(content,"text/html")
        msg.send()

    def gen_verification_token(self,user):
        """ Create a JWT token that the user will use to verify their account """
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user':user.username,
            'exp':int(exp_date.timestamp()),
            'type':'email_confirmation',
        }

        token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')

        return token