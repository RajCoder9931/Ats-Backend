from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.contract_model import (
    create_contract_from_lead,
    get_all_contracts,
    get_contract_by_id,
    deactivate_contract
)

contract_bp = Blueprint(
    "contracts",
    __name__,
    url_prefix="/api/contracts"
)


# ================= CONVERT LEAD TO CONTRACT =================
@contract_bp.route("/convert/<lead_id>", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def convert_lead_to_contract(lead_id):
    created_by = request.user.get("id")

    contract, error = create_contract_from_lead(lead_id, created_by)

    if error:
        return jsonify({"message": error}), 400

    if not contract:
        return jsonify({"message": "Failed to convert lead to contract"}), 500

    return jsonify({
        "message": "Lead converted to contract successfully",
        "contract": contract
    }), 201


# ================= GET ALL CONTRACTS =================
@contract_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_all_contracts():
    contracts = get_all_contracts()
    return jsonify(contracts), 200


# ================= GET CONTRACT BY ID =================
@contract_bp.route("/<contract_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_contract_by_id(contract_id):
    contract = get_contract_by_id(contract_id)

    if not contract:
        return jsonify({"message": "Contract not found"}), 404

    return jsonify(contract), 200


# ================= DEACTIVATE CONTRACT =================
@contract_bp.route("/deactivate/<contract_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate_contract_api(contract_id):
    success = deactivate_contract(contract_id)

    if not success:
        return jsonify({"message": "Contract not found"}), 404

    return jsonify({"message": "Contract deactivated successfully"}), 200
