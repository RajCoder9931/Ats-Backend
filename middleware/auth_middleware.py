from functools import wraps
from flask import request, jsonify
from utils.jwt_utils import decode_token


def auth_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"message": "Authorization header missing"}), 401

            if not auth_header.startswith("Bearer "):
                return jsonify({"message": "Invalid auth header format"}), 401

            token = auth_header.split(" ", 1)[1]

            try:
                payload = decode_token(token)
                user_role = payload.get("role")

                if allowed_roles and user_role not in allowed_roles:
                    return jsonify({"message": "Access denied"}), 403

                
                request.user = {
                    "id": payload.get("id"),
                    "role": user_role,
                }

            except Exception as e:
                return jsonify({"message": "Invalid or expired token"}), 401

            return f(*args, **kwargs)

        return wrapper
    return decorator
