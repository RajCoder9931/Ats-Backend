from flask import Blueprint, jsonify
from middleware.auth_middleware import auth_required
from models.dashboard_stats_model import get_dashboard_stats

dashboard_stats_bp = Blueprint("dashboard_stats", __name__, url_prefix="/api/dashboard")

@dashboard_stats_bp.route("/stats-leads", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_dashboard_stats():
    stats = get_dashboard_stats()
    return jsonify(stats), 200
