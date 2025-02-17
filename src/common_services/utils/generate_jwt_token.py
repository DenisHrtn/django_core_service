import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_core_service.settings")
django.setup()

from datetime import timedelta  # noqa

from rest_framework_simplejwt.tokens import AccessToken  # noqa

SECRET_KEY = "BZdZBJCPXomiijXAbNqNrx0ihDBofzqH"
ALGORITHM = "HS256"


def generate_jwt_token(user_id=1, role_name="admin", email="test@gmail.com"):
    token = AccessToken()
    token["user_id"] = user_id
    token["role_name"] = role_name
    token["email"] = email
    token.set_exp(lifetime=timedelta(hours=1))

    return str(token)


mock_token = generate_jwt_token()
print(mock_token)
