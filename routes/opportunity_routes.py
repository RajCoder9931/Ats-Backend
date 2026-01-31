from flask import Blueprint, request, jsonify
from bson.errors import InvalidId
from middleware.auth_middleware import auth_required
from models.opportunity_model import (
    create_opportunity,
    create_opportunity_from_contract,
    get_active_opportunities,
    get_inactive_opportunities,
    get_opportunity_by_id,
    deactivate_opportunity,
    activate_opportunity
)

opportunity_bp = Blueprint(
    "opportunities",
    __name__,
    url_prefix="/api/opportunities"
)



@opportunity_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_opportunity():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"message": "Invalid or missing JSON body"}), 400

        required_fields = ["companyName", "jobTitle", "jobDescription", "numberOfOpenings"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"{field} is required"}), 400

        data["createdBy"] = request.user.get("id")

        opp = create_opportunity(data)

        if not opp:
            return jsonify({"message": "Failed to create opportunity"}), 500

        return jsonify({
            "message": "Opportunity created successfully",
            "opportunity": opp
        }), 201

    except InvalidId:
        return jsonify({"message": "Invalid ID format"}), 400

    except Exception as e:
        print("Add opportunity error:", str(e))
        return jsonify({"message": "Server error while creating opportunity"}), 500



@opportunity_bp.route("/convert/<contract_id>", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def convert_contract_to_opportunity(contract_id):
    created_by = request.user.get("id")

    try:
        opp, error = create_opportunity_from_contract(contract_id, created_by)

        if error:
            return jsonify({"message": error}), 400

        if not opp:
            return jsonify({"message": "Failed to convert contract to opportunity"}), 500

        return jsonify({
            "message": "Contract converted to opportunity successfully",
            "opportunity": opp
        }), 201

    except InvalidId:
        return jsonify({"message": "Invalid contract id format"}), 400

    except Exception as e:
        print("Convert contract error:", str(e))
        return jsonify({"message": "Server error while converting contract"}), 500



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
