from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.user_model import (
    find_by_id,
    update_user,
    change_user_password
)
from utils.password_utils import check_password

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


@user_bp.route("/me", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def get_me():
    user = find_by_id(request.user["id"])

    if not user:
        return jsonify({"message": "User not found"}), 404

    user["_id"] = str(user["_id"])
    user.pop("password", None)
    user.pop("refresh_token", None)

    return jsonify(user), 200


@user_bp.route("/me", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin"])
def update_profile():
    data = request.json
    allowed_fields = ["name", "email", "phone"]

    update_data = {
        field: data[field]
        for field in allowed_fields
        if data.get(field)
    }

    if not update_data:
        return jsonify({"message": "Nothing to update"}), 400

    user = update_user(request.user["id"], update_data)

    user["_id"] = str(user["_id"])
    user.pop("password", None)
    user.pop("refresh_token", None)

    return jsonify(user), 200


@user_bp.route("/change-password", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin"])
def change_password():
    data = request.json

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")
    confirm_password = data.get("confirmPassword")

    if not all([current_password, new_password, confirm_password]):
        return jsonify({"message": "All fields required"}), 400

    if new_password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    user = find_by_id(request.user["id"])

    if not check_password(current_password, user["password"]):
        return jsonify({"message": "Current password incorrect"}), 401

    change_user_password(request.user["id"], new_password)

    return jsonify({"message": "Password updated successfully"}), 200
