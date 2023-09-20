from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.db import models


class User(AbstractUser):
    """Пользовательская модель юзера."""

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[username_validator, MinLengthValidator(3)],
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        max_length=255,
    )
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    class Meta(AbstractUser.Meta):
        ordering = ("-id",)


class Friend(models.Model):
    user = models.ForeignKey(
        User,
        related_name="friend_init",
        on_delete=models.CASCADE,
        db_column="user_id"
    )
    friend = models.ForeignKey(
        User,
        related_name="friend_subs",
        on_delete=models.CASCADE,
        db_column="friend_id",
    )

    class Meta:
        verbose_name = "Друг"
        verbose_name_plural = "Друзья"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "friend"],
                name="unique_friend",
            ),
        ]


class Session(models.Model):
    user = models.ForeignKey(
        User,
        editable=False,
        related_name="sessions",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        db_column="user_id"
    )
    jwt_token = models.CharField(
        "Токен",
        editable=False,
        max_length=256,
        null=False,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, editable=False)
    expires_at = models.DateTimeField("Годен до:", auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"

    def __str__(self):
        return f"Session {self.id}: {self.user.username}"
