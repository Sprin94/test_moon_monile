from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post
from posts.api.serializers import PostCreateSerializer


class PostCreateAPIView(CreateAPIView):
    """Создание Post"""

    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "Post created successfully",
                "post_id": serializer.data['id'],
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
