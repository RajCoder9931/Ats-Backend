from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.contact_log_model import (
    create_contact_log,
    get_active_logs,
    get_inactive_logs,
    get_log_by_id,
    deactivate_log,
    activate_log
)

contact_log_bp = Blueprint(
    "contact_logs",
    __name__,
    url_prefix="/api/contact-logs"
)



@contact_log_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_contact_log():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required_fields = ["communicationType", "subject"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    
    if not data.get("leadId") and not data.get("contractId"):
        return jsonify({"message": "leadId or contractId is required"}), 400

    data["createdBy"] = request.user.get("id")

    log = create_contact_log(data)

    if not log:
        return jsonify({"message": "Failed to create contact log"}), 500

    return jsonify(log), 201



@contact_log_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_logs():
    logs = get_active_logs()
    return jsonify(logs), 200



@contact_log_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_logs():
    logs = get_inactive_logs()
    return jsonify(logs), 200



@contact_log_bp.route("/<log_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_log_by_id(log_id):
    log = get_log_by_id(log_id)

    if not log:
        return jsonify({"message": "Contact log not found"}), 404

    return jsonify(log), 200



@contact_log_bp.route("/deactivate/<log_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(log_id):
    success = deactivate_log(log_id)

    if not success:
        return jsonify({"message": "Contact log not found"}), 404

    return jsonify({"message": "Contact log deactivated successfully"}), 200



@contact_log_bp.route("/activate/<log_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(log_id):
    success = activate_log(log_id)

    if not success:
        return jsonify({"message": "Contact log not found"}), 404

    return jsonify({"message": "Contact log activated successfully"}), 200
