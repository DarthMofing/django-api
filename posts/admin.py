""" Post Admin Config """

from django.contrib import admin

#Models
from posts.models import Post

@admin.register(Post)
class PostsAdmin(admin.ModelAdmin):

    list_display = ['title', 'image', 'likes']
    list_display_links = ['title']
    list_editable = ['image', 'likes']
    search_fields = ['created_at']
    list_filter = ['created_at']
