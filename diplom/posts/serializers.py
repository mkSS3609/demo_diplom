from rest_framework import serializers

from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at', 'post']
        read_only_fields = ['id', 'author', 'created_at', 'post']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError('Текст отсутствует!')
        return value


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(read_only=True, source='likes_count')
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image', 'created_at', 'author', 'comments', 'likes_count']
        read_only_fields = ['id', 'created_at', 'author', 'comments', 'likes_count']

    def validate(self, value):
        request = self.context.get('request')
        if request and not request.user.is_authenticated:
            raise serializers.ValidationError('Требуется аутентификация')
        return value


class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'image']
        read_only_fields = ['id']

    def validate_text(self, value):
        if not value.strip() and not self.initial_data.get('image'):
            raise serializers.ValidationError('Пост пустой!')


# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(read_only=True, slug_field='username')
#     post = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Like
#         fields = ['id', 'post', 'user']
#         read_only_fields = ['id', 'post', 'user']