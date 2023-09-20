from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, InvalidToken):
        response_data = {"error": "Unauthorized", "message": "Invalid token"}
        return Response(response_data, status=401)
    elif isinstance(exc, NotAuthenticated):
        response_data = {"error": "Unauthorized", "message": exc.default_detail}
        return Response(response_data, status=401)
    elif isinstance(exc, (NotFound, Http404)):
        response_data = {
            "error": "Not Found"
        }
        return Response(response_data, status=404)

    return exception_handler(exc, context)
