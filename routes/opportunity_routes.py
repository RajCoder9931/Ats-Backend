from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.opportunity_model import (
    create_opportunity,
    get_active_opportunities,
    get_inactive_opportunities,
    get_opportunity_by_id,
    deactivate_opportunity,
    activate_opportunity
)

opportunity_bp = Blueprint("opportunities", __name__, url_prefix="/api/opportunities")


@opportunity_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_opportunity():
    data = request.get_json()

    required_fields = ["leadId", "companyName", "jobTitle", "jobDescription", "numberOfOpenings"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

    data["createdBy"] = request.user.get("id")

    opp = create_opportunity(data)
    return jsonify(opp), 201



@opportunity_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_opportunities():
    opps = get_active_opportunities()
    return jsonify(opps), 200



@opportunity_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_opportunities():
    opps = get_inactive_opportunities()
    return jsonify(opps), 200



@opportunity_bp.route("/<opp_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_opportunity_by_id(opp_id):
    opp = get_opportunity_by_id(opp_id)

    if not opp:
        return jsonify({"message": "Opportunity not found"}), 404

    return jsonify(opp), 200



@opportunity_bp.route("/deactivate/<opp_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(opp_id):
    success = deactivate_opportunity(opp_id)

    if not success:
        return jsonify({"message": "Opportunity not found"}), 404

    return jsonify({"message": "Opportunity deactivated successfully"}), 200



@opportunity_bp.route("/activate/<opp_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(opp_id):
    success = activate_opportunity(opp_id)

    if not success:
        return jsonify({"message": "Opportunity not found"}), 404

    return jsonify({"message": "Opportunity activated successfully"}), 200
