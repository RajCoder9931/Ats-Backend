import jwt
import datetime
from config import JWT_SECRET, ACCESS_TOKEN_MINUTES, REFRESH_TOKEN_DAYS


def generate_access_token(user):
    """
    Used by ADMIN / SUPER ADMIN
    """
    payload = {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],   # admin / super_admin
        "type": "access",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def generate_refresh_token(user):
    """
    ADMIN ONLY
    """
    payload = {
        "id": str(user["_id"]),
        "role": user["role"],
        "type": "refresh",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=REFRESH_TOKEN_DAYS),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def generate_candidate_token(user):
    """
    CANDIDATE ONLY (NO REFRESH TOKEN)
    """
    payload = {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": "candidate",
        "type": "candidate",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
