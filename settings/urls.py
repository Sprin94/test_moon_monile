from django.contrib import admin
from django.urls import include, path

api_urlpatterns = [
    path("posts/", include(("posts.api.urls", "posts"))),
    path("users/", include(("users.api.urls", "users"))),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]
