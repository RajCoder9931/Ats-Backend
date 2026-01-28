from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.job_posting_model import (
    create_job_posting,
    get_active_job_postings,
    get_inactive_job_postings,
    get_job_posting_by_id,
    deactivate_job_posting,
    activate_job_posting
)

job_posting_bp = Blueprint("job_postings", __name__, url_prefix="/api/job-postings")


@job_posting_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_job_posting():
    data = request.get_json()

    required_fields = ["opportunityId", "companyName", "jobTitle", "jobDescription", "numberOfOpenings"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

    data["createdBy"] = request.user.get("id")

    job = create_job_posting(data)
    return jsonify(job), 201


@job_posting_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_job_postings():
    jobs = get_active_job_postings()
    return jsonify(jobs), 200


@job_posting_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_job_postings():
    jobs = get_inactive_job_postings()
    return jsonify(jobs), 200


@job_posting_bp.route("/<job_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_job_posting_by_id(job_id):
    job = get_job_posting_by_id(job_id)

    if not job:
        return jsonify({"message": "Job posting not found"}), 404

    return jsonify(job), 200


@job_posting_bp.route("/deactivate/<job_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(job_id):
    success = deactivate_job_posting(job_id)

    if not success:
        return jsonify({"message": "Job posting not found"}), 404

    return jsonify({"message": "Job posting deactivated successfully"}), 200


@job_posting_bp.route("/activate/<job_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(job_id):
    success = activate_job_posting(job_id)

    if not success:
        return jsonify({"message": "Job posting not found"}), 404

    return jsonify({"message": "Job posting activated successfully"}), 200
