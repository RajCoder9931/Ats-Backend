from flask import Blueprint, jsonify, request
from middleware.auth_middleware import auth_required
from models.candidate_dashboard_model import get_candidate_dashboard_stats

candidate_dashboard_bp = Blueprint(
    "candidate_dashboard",
    __name__,
    url_prefix="/api/candidate/dashboard"
)

@candidate_dashboard_bp.route("/stats", methods=["GET"])
@auth_required(allowed_roles=["candidate"])
def candidate_dashboard_stats():
    candidate_id = request.user.get("id")
    stats = get_candidate_dashboard_stats(candidate_id)
    return jsonify(stats), 200
