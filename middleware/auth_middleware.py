from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Authorization header missing"}), 401

        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Invalid auth header format"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = decode_token(token)

            request.user = {
                "id": payload.get("id"),
                "role": payload.get("role"),
            }
        except Exception as e:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated
