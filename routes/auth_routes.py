from flask import Blueprint, request, jsonify
from models.user_model import (
    find_by_email,
    create_user,
    save_refresh_token,
    find_by_refresh_token,
    remove_refresh_token
)
from utils.password_utils import hash_password, check_password
from utils.jwt_utils import (
    generate_access_token,
    generate_refresh_token,
    decode_token
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not all([name, email, password, role]):
        return jsonify({"message": "All fields required"}), 400

    if find_by_email(email):
        return jsonify({"message": "User already exists"}), 400

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "role": role
    }

    result = create_user(user)
    user["_id"] = result.inserted_id

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    save_refresh_token(user["_id"], refresh_token)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "name": name,
            "email": email,
            "role": role
        }
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = find_by_email(email)
    if not user or not check_password(password, user["password"]):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    save_refresh_token(user["_id"], refresh_token)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })

@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    data = request.json
    token = data.get("refresh_token")

    if not token:
        return jsonify({"message": "Refresh token required"}), 400

    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            return jsonify({"message": "Invalid token"}), 401
    except:
        return jsonify({"message": "Invalid or expired refresh token"}), 401

    user = find_by_refresh_token(token)
    if not user:
        return jsonify({"message": "Token revoked"}), 401

    new_access = generate_access_token(user)
    return jsonify({"access_token": new_access})

@auth_bp.route("/logout", methods=["POST"])
def logout():
    data = request.json
    token = data.get("refresh_token")
    user = find_by_refresh_token(token)
    if user:
        remove_refresh_token(user["_id"])
    return jsonify({"message": "Logged out"})
