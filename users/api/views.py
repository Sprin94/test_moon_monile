from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.exceptions import AuthenticationFailed, ParseError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from users.api.serializers import FriendSerializer, UserSerializer
from users.models import Friend, Session

User = get_user_model()


class UserCreateApiView(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomAuthToken(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except AuthenticationFailed:
            raise ParseError(
                {"error": "Bad Request", "message": "Invalid username or password"},
                code=status.HTTP_400_BAD_REQUEST,
            )
        except TokenError:
            raise InvalidToken({"error": "Unauthorized", "message": "Invalid token"})

        session = Session(
            user=serializer.user,
            jwt_token=serializer.validated_data['access'],
            expires_at=serializer.refresh['exp'],
        )
        session.save()

        return Response(
            {
                "message": "Logged in successfully",
                "username": serializer.user.username
            },
            headers={"Authorization": f"Bearer {serializer.validated_data['access']}"}
        )


class UserRetrieveAPIView(RetrieveAPIView):
    """Просмотр User"""

    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FriendCreateDestroyAPIView(CreateAPIView, DestroyAPIView):
    """Создание Friend"""

    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "message": "Friend added successfully",
            "friend_username": kwargs.get('username')
        }
        return response

    def destroy(self, request, *args, **kwargs):
        friend = get_object_or_404(User, username=kwargs.get('username'))
        relation = Friend.objects.filter(user=request.user, friend=friend)
        if relation:
            relation.delete()
            return Response(
                {
                    "message": "Friend removed successfully",
                    "friend_username": friend.username
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response({"errors": "Вы не дружите"})


class DeactivateUserView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, nickname):
        try:
            user = User.objects.get(nickname=nickname)

            user.is_active = False
            user.save()
            return Response(
                {"message": "Пользователь успешно деавторизован"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Пользователь не найден"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                {"message": "Ошибка деавторизации пользователя"},
                status=status.HTTP_400_BAD_REQUEST
            )


class DeleteSession(APIView):
    def delete(self, request, format=None):
        auth_header = request.META.get("HTTP_AUTHORIZATION").split()[1]
        Session.objects.filter(jwt_token=auth_header).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
