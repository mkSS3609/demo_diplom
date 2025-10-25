from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from diplom.posts.views import PostViewSet # пиздц какой-то -- ModuleNotFoundError: No module named 'diplom.posts' (типо какого хуя)

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
] + router.urls
