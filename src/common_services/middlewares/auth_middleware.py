import redis
from django.conf import settings
from django.http import JsonResponse

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


class TokenMiddleware:
    """
    Middleware, который проверяет наличие токена в Redis.
    Если токен не найден, перенаправляет пользователя.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get("Authorization")
        token = token.split(" ")[1]
        print(token)
        if not token:
            return JsonResponse(
                {"error": "Token is missing in the request header"}, status=400
            )

        if not redis_client.exists(f"token:{token}"):
            return JsonResponse({"error": "Token is invalid or expired"}, status=401)

        response = self.get_response(request)
        return response
