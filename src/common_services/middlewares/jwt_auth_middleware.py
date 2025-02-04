import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JWTAuthMiddleware(MiddlewareMixin):
    """
    Мидлваря для реализации авторизации
    запросов пльзователя с Auth на Core.
    По сути выполняет ту же роль, что и
    встроенная от Django REST, но здесь
    еще делаем доп провеку на payload.
    """

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse(
                {"error": "Токен не найден или неверный формат"}, status=401
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=["HS256"])
            request.user_id = payload.get("user_id")
            request.user_role = payload.get("role")
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Токен истёк"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Неверный токен"}, status=401)
