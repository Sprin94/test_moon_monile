from rest_framework import serializers

from users.utils import UserDefault
from posts.models import Post


class PostGetSerializer(serializers.ModelSerializer):
    """Сериализатор для GET"""
    post_id = serializers.IntegerField(source="id")
    author = serializers.CharField(source='user.username')

    class Meta:
        model = Post
        fields = [
            'post_id',
            'title',
            'content',
            'author'
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания постов"""

    wall_owner = serializers.HiddenField(default=UserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = [
            'wall_owner',
            'title',
            'content',
            'id',
            'user'
        ]
