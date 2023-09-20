from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import APIException

from users.models import Friend, User
from users.utils import UserDefault
from posts.api.serializers import PostGetSerializer


class UserExist(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'User already exists.'
    default_code = 'Conflict'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        required=True,
    )
    posts = PostGetSerializer(many=True, source="wall_posts", read_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "username",
            "email",
            "posts",
        )

    def is_valid(self, *, raise_exception=False):
        if raise_exception and User.objects.filter(
            Q(username=self.initial_data["username"])
            | Q(email=self.initial_data["email"])
        ):
            raise UserExist(
                {"error": "Conflict", "message": "User already exists"}
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class FriendSerializer(serializers.ModelSerializer):
    friend = serializers.HiddenField(default=UserDefault())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Friend
        fields = (
            "friend",
            "user"
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Friend.objects.all(),
                fields=["user", "friend"],
                message="Вы уже дружите.",
            ),
        ]

    def validate(self, attrs):
        if self.context.get("request").user == attrs.get("friend"):
            raise serializers.ValidationError(
                "Нельзя дружить с собой",
            )
        return super().validate(attrs)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        self.refresh = self.get_token(self.user)

        data["refresh"] = str(self.refresh)
        data["access"] = str(self.refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
