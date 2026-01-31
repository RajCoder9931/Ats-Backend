from flask import Blueprint, request, jsonify
from functools import wraps
from models.user_model import find_by_email, create_user
from utils.password_utils import hash_password, check_password
from utils.jwt_utils import generate_access_token, decode_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token is missing"}), 401

        token = auth_header.split(" ")[1]

        try:
            payload = decode_token(token)

            if payload.get("type") != "access":
                return jsonify({"message": "Invalid token type"}), 401

            request.user = payload

        except Exception:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)

    return decorated



@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password, role]):
        return jsonify({"message": "All fields required"}), 400

    if find_by_email(email):
        return jsonify({"message": "User already exists"}), 409

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": role
    }

    created_user = create_user(user)
    if not created_user:
        return jsonify({"message": "User creation failed"}), 500

    access_token = generate_access_token(created_user)

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": created_user["_id"],
            "name": created_user["name"],
            "email": created_user["email"],
            "role": created_user["role"]
        }
    }), 201



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # optional

    if not all([email, password]):
        return jsonify({"message": "Email and password required"}), 400

    user = find_by_email(email)

    if not user or not check_password(password, user["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    
    if role and user["role"] != role:
        return jsonify({"message": "Invalid role for this user"}), 403

    access_token = generate_access_token(user)

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user["_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile():
    return jsonify({
        "message": "Profile accessed successfully",
        "user": request.user
    }), 200
