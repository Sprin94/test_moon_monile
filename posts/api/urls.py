from django.urls import path

from posts.api.views import PostCreateAPIView

app_name = 'posts'

urlpatterns = [
    path("<str:username>/", PostCreateAPIView.as_view())
]
