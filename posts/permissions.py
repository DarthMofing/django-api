""" Post permissions class """

# Django REST framework
from rest_framework.permissions import BasePermission

# Models
from posts.models import Author, Post

class IsAuthor(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        """ Permission that verifies if the user is the author of the post """

        try:
            Author.objects.get(author=request.user, post=Post.objects.get(pk=obj.pk))
        except Author.DoesNotExist:
            return False
            
        return True