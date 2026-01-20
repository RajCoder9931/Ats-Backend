from flask import Blueprint, jsonify, request
from middleware.auth_middleware import auth_required
from models.notification_model import (
    get_user_notifications,
    mark_notification_read
)

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/api/notifications"
)


@notification_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def fetch_notifications():
    user_id = request.user.get("id")
    data = get_user_notifications(user_id)
    return jsonify(data), 200


@notification_bp.route("/<notification_id>/read", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin"])
def read_notification(notification_id):
    mark_notification_read(notification_id)
    return jsonify({"message": "Notification marked as read"}), 200
