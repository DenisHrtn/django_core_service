import datetime

import jwt

SECRET_KEY = "BZdZBJCPXomiijXAbNqNrx0ihDBofzqH"
ALGORITHM = "HS256"


def generate_jwt_token(user_id=1, role_name="admin", email="test2@example.com"):
    payload = {
        "user_id": user_id,
        "role_name": role_name,
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


mock_token = generate_jwt_token()
print(mock_token)
