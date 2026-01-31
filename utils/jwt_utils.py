import jwt
import datetime
from config import JWT_SECRET, ACCESS_TOKEN_MINUTES
from jwt import ExpiredSignatureError, InvalidTokenError


def generate_access_token(user):
    payload = {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "role": user.get("role"),
        "type": "access",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # PyJWT >= 2.0 returns str, older returns bytes
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def generate_candidate_token(user):
    payload = {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "role": "candidate",
        "type": "access",
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload

    except ExpiredSignatureError:
        raise Exception("Token expired")

    except InvalidTokenError:
        raise Exception("Invalid token")
