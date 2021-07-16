""" Profile - BaseUser Model"""
from django.db import models
from django.contrib.auth.models import User

class Profile (models.Model):

    """ Adding data to Base User Model """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,null=True)
    hero_badge = models.ImageField(blank=True,null=True)
    age = models.IntegerField()
    city = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=100,blank=True,null=True)
    followers = models.IntegerField()
    likes = models.IntegerField()
    posts = models.IntegerField()

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.user.get_full_name()
