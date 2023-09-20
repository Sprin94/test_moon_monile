from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Friend, User, Session


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админ модель User."""


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    """Админ модель Friend."""


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Админ модель Session."""
    readonly_fields = ('user', 'jwt_token', 'created_at', 'expires_at')
