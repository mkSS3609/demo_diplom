from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from diplom.posts.models import Post, Comment, Like
from diplom.posts.serializers import PostSerializer, PostCreateSerializer, CommentSerializer


# Create your views here.

# class IsOwnerOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.author == request.user # возможно user

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('author').prefetch_related('comments', 'likes')
    serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return PostCreateSerializer
#         return PostSerializer
#
#     def perform_create(self, serializer):
#         if not self.request.user.is_authenticated:
#             raise PermissionDenied(detail='Требуется аутентификация')
#         serializer.save(author=self.request.user)
#
#     def perform_update(self, serializer):
#         serializer.save(author=self.request.user)
#
#     def like(self, request, pk=None):
#         post = self.get_object()
#         like, created = Like.objects.get_or_create(post=post, user=request.user)
#         if not created:
#             like.delete()
#             return Response({'status': 'unliked', 'likes_count': post.likes_count()}, status=status.HTTP_200_OK)
#         return Response({'status': 'liked', 'likes_count': post.likes_count()}, status=status.HTTP_201_CREATED)
#
#     def unlike(self, request, pk=None):
#         post = self.get_object()
#         like = Like.objects.filter(post=post, user=request.user).first()
#         if like:
#             like.delete()
#             return Response({'status': 'unliked', 'likes_count': post.likes_count()}, status=status.HTTP_200_OK)
#         return Response({'datail': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             return super().retrieve(request, *args, **kwargs)
#         except Post.DoesNotExist:
#             raise NotFound(detail='Пост не найден')
#
#
# class CommentViewSet(GenericViewSet):
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get_queryset(self):
#         post_id = self.kwargs.get('post_id')
#         return Comment.objects.filter(post_id=post_id).select_related('author')
#
#     def perform_create(self, serializer):
#         post_id = self.kwargs.get('post_id')
#         post = Post.objects.get(id=post_id)
#         serializer.save(author=self.request.user, post=post)