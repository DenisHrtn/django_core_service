import jwt
from django.conf import settings
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed


def decode_jwt_token(request: HttpRequest):
    """
    Функция для декодирования JWT-токена пришедшего с Auth-сервиса
    :param request:
    :return: user_id, role_name, email
    """

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("Токен не найден или неверного формата")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise AuthenticationFailed("Срок действия токена истёк") from exc
    except jwt.InvalidTokenError as exc:
        raise AuthenticationFailed("Неверный токен") from exc

    return payload.get("user_id"), payload.get("role_name"), payload.get("email")
