from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.job_application_model import (
    has_already_applied,
    apply_for_job,
    get_applied_jobs_by_candidate
)
from models.job_model import get_job_by_id

job_application_bp = Blueprint(
    "job_applications",
    __name__,
    url_prefix="/api"
)


@job_application_bp.route("/jobs/<job_id>/apply", methods=["POST"])
@auth_required(allowed_roles=["candidate"])
def apply_job(job_id):
    candidate_id = request.user.get("id")

    job = get_job_by_id(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    if has_already_applied(job_id, candidate_id):
        return jsonify({"message": "Already applied to this job"}), 409

    application = apply_for_job(job_id, candidate_id)

    if not application:
        return jsonify({"message": "Failed to apply for job"}), 500

    return jsonify({
        "message": "Job applied successfully",
        "application": application
    }), 201



@job_application_bp.route("/candidate/applied-jobs", methods=["GET"])
@auth_required(allowed_roles=["candidate"])
def get_applied_jobs():
    candidate_id = request.user.get("id")

    jobs = get_applied_jobs_by_candidate(candidate_id)

    return jsonify({
        "count": len(jobs),
        "jobs": jobs
    }), 200
