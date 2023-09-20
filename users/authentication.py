from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from users.models import Session


class MyJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        if not Session.objects.filter(
            user_id=validated_token['user_id'],
            jwt_token=raw_token.decode()
        ):
            raise InvalidToken

        return self.get_user(validated_token), validated_token
