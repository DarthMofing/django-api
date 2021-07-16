
from django.contrib import admin
from django.db import router
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from users.views import users as users_views
from users.views.login import UserLoginAPIView as login
from posts.views import PostsViewSet

#Django REST framework
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts',PostsViewSet, basename='posts')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', users_views.UserListView.as_view(), name='users'),
    path('users/login/', login.as_view(), name='login'),
    path('users/signup/', users_views.signup, name='signup'),
    path('users/verify/', users_views.account_verification, name='verify'),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
