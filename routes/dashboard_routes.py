from flask import Blueprint, jsonify, request
from middleware.auth_middleware import auth_required
from models.dashboard_model import get_dashboard_stats

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)

@dashboard_bp.route("/stats", methods=["GET"])
@auth_required
def dashboard_stats():
    stats = get_dashboard_stats(request.user.get("id"))
    return jsonify(stats), 200
