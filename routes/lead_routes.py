from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.contract_model import create_contract_from_lead
from models.lead_model import (
    create_lead,
    get_active_leads,
    get_inactive_leads,
    get_lead_by_id,
    deactivate_lead,
    activate_lead,
    update_lead
)

lead_bp = Blueprint("leads", __name__, url_prefix="/api/leads")


@lead_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_lead():
    data = request.get_json()

    required_fields = [
        "companyName",
        "companyOwnerName",
        "companyEmail",
        "companyPhone",
        "contactName",
        "contactEmail"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

    data["createdBy"] = request.user.get("id")

    lead = create_lead(data)
    return jsonify(lead), 201


@lead_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_leads():
    leads = get_active_leads()
    return jsonify(leads), 200


@lead_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_leads():
    leads = get_inactive_leads()
    return jsonify(leads), 200


@lead_bp.route("/<lead_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_lead_by_id(lead_id):
    lead = get_lead_by_id(lead_id)

    if not lead:
        return jsonify({"message": "Lead not found"}), 404

    return jsonify(lead), 200


@lead_bp.route("/<lead_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def update_lead_api(lead_id):
    data = request.get_json()

    success = update_lead(lead_id, data)

    if not success:
        return jsonify({"message": "Lead not found or no changes made"}), 404

    return jsonify({"message": "Lead updated successfully"}), 200


@lead_bp.route("/deactivate/<lead_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(lead_id):
    success = deactivate_lead(lead_id)

    if not success:
        return jsonify({"message": "Lead not found"}), 404

    return jsonify({"message": "Lead deactivated successfully"}), 200


@lead_bp.route("/activate/<lead_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(lead_id):
    success = activate_lead(lead_id)

    if not success:
        return jsonify({"message": "Lead not found"}), 404

    return jsonify({"message": "Lead activated successfully"}), 200

@lead_bp.route("/convert/<lead_id>", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def convert_lead(lead_id):
    created_by = request.user.get("id")

    contract, error = create_contract_from_lead(lead_id, created_by)

    if error:
        return jsonify({"message": error}), 400

    return jsonify({
        "message": "Lead converted to contract",
        "contract": contract
    }), 201