""" Posts model serializer """

#Django REST framework
from rest_framework import serializers

#Models
from django.contrib.auth.models import User
from posts.models import Author, Post

class PostModelSerializer(serializers.ModelSerializer):
    """ Post model serializer """

    class Meta:
        model=Post
        fields = ['pk', 'image', 'title', 'likes', 'created_at']

class GetAuthorSerializer(serializers.ModelSerializer):
    """ Get the username from the user model """
    
    class Meta:
        model = User
        fields = ['username']    

class AuthorModelSerializer(serializers.ModelSerializer):
    """ Author model serializer """

    author = GetAuthorSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ['author', 'post']
        depth = 1