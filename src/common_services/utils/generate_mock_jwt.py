import datetime

import jwt

SECRET_KEY = "BZdZBJCPXomiijXAbNqNrx0ihDBofzqH"
ALGORITHM = "HS256"


def generate_mock_jwt(user_id=1, role_name="admin", email="test@example.com"):
    payload = {
        "user_id": user_id,
        "role_name": role_name,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


mock_token = generate_mock_jwt()
print(mock_token)
