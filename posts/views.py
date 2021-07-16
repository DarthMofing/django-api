""" Posts ViewSet """

# Django REST framework
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Permissions
from posts.permissions import IsAuthor

# Models
from posts.models import Post, Author

# Serializer
from posts.serializer import AuthorModelSerializer, PostModelSerializer


class PostsViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """ Posts Model ViewSet """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        """ Save post's author """
        post = serializer.save()
        user = self.request.user
        Author.objects.create(user=user, post=post)

    def get_permissions(self):
        """ Assign permissions based on action """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions.append(IsAuthor)
            
        return [permission() for permission in permissions]

    def retrieve(self, request, *args, **kwargs):
        """ Bring the data of the post with the author """
        instance = self.get_object()
        author = Author.objects.get(post=instance.pk)
        serializer = AuthorModelSerializer(author)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """ Lists all posts data with their authors """
        queryset = Author.objects.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = AuthorModelSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AuthorModelSerializer(queryset, many=True)
        return Response(serializer.data)
