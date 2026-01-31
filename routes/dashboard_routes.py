from flask import Blueprint, jsonify, request
from middleware.auth_middleware import auth_required
from models.dashboard_model import get_dashboard_stats

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


@dashboard_bp.route("/stats", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def dashboard_stats():
    user_id = request.user.get("id")

    stats = get_dashboard_stats(user_id)

    if not stats:
        return jsonify({"message": "Failed to fetch dashboard stats"}), 500

    return jsonify(stats), 200
