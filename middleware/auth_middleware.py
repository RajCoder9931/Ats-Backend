# middleware/auth_middleware.py
from functools import wraps
from flask import request, jsonify
import jwt
from config import JWT_SECRET

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Unauthorized"}), 401

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = payload
        except:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper
