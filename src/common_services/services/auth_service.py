import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):
    """
    Кастомный сервис, где Django не пытается найти
    юзера в БД, а просто возвращает payload
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationFailed("Срок действия токена истёк") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationFailed("Неверный токен") from exc

        return payload, None
