from django.urls import path

from users.api.views import (
    FriendCreateDestroyAPIView,
    UserRetrieveAPIView,
    UserCreateApiView,
    CustomAuthToken,
    DeactivateUserView,
    DeleteSession,
)

urlpatterns = [
    path(
        "friend/<str:username>/",
        FriendCreateDestroyAPIView.as_view(http_method_names=("post",))
    ),
    path(
        "unfriend/<str:username>/",
        FriendCreateDestroyAPIView.as_view(http_method_names=("delete",))
    ),
    path(
        "profile/<str:username>/",
        UserRetrieveAPIView.as_view()
    ),
    path(
        "register/",
        UserCreateApiView.as_view(),
    ),
    path("login/", CustomAuthToken.as_view()),
    path("logout/", DeleteSession.as_view()),
    path('deactivate/<username>', DeactivateUserView.as_view()),
]
