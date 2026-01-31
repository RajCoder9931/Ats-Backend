from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.job_posting_model import (
    create_job_posting_from_opportunity,
    get_all_job_postings,
    get_active_job_postings,
    get_inactive_job_postings,
    get_job_posting_by_id,
    get_job_posting_by_opportunity_id
)

job_posting_bp = Blueprint(
    "job_postings",
    __name__,
    url_prefix="/api/job-postings"
)

@job_posting_bp.route("/convert/<opportunity_id>", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def convert_opportunity_to_job(opportunity_id):
    user = getattr(request, "user", None)
    user_id = user.get("id") if user else None

    job = create_job_posting_from_opportunity(opportunity_id, user_id)

    if job == "EXISTS":
        return jsonify({
            "message": "Job posting already exists for this opportunity"
        }), 409

    if not job:
        return jsonify({
            "message": "Opportunity not found or inactive"
        }), 404

    return jsonify({
        "message": "Job posting created successfully",
        "job": job
    }), 201


@job_posting_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_all_jobs():
    jobs = get_all_job_postings()
    return jsonify(jobs), 200


@job_posting_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_jobs():
    jobs = get_active_job_postings()
    return jsonify(jobs), 200


@job_posting_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_jobs():
    jobs = get_inactive_job_postings()
    return jsonify(jobs), 200


@job_posting_bp.route("/<job_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_job_by_id(job_id):
    job = get_job_posting_by_id(job_id)

    if not job:
        return jsonify({"message": "Job posting not found"}), 404

    return jsonify(job), 200


@job_posting_bp.route("/by-opportunity/<opportunity_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_job_by_opportunity(opportunity_id):
    job = get_job_posting_by_opportunity_id(opportunity_id)

    if not job:
        return jsonify({
            "message": "No job posting found for this opportunity"
        }), 404

    return jsonify(job), 200
