from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


class UserDefault(object):
    requires_context = True
    model = get_user_model()

    def __call__(self, serializer_field):
        view = serializer_field.context['view']
        username = view.kwargs.get("username")
        return get_object_or_404(self.model, username=username)
