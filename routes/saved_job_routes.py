from flask import Blueprint, jsonify, request
from middleware.auth_middleware import auth_required
from models.saved_job_model import (
    is_job_saved,
    save_job,
    remove_saved_job,
    get_saved_jobs
)
from models.job_model import get_job_by_id

saved_job_bp = Blueprint(
    "saved_jobs",
    __name__,
    url_prefix="/api/candidate/jobs"
)

@saved_job_bp.route("/<job_id>/save", methods=["POST"])
@auth_required(allowed_roles=["candidate"])
def save_job_route(job_id):
    candidate_id = request.user.get("id")

    job = get_job_by_id(job_id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    if is_job_saved(candidate_id, job_id):
        return jsonify({"message": "Job already saved"}), 409

    save_job(candidate_id, job_id)

    return jsonify({"message": "Job saved successfully"}), 201


@saved_job_bp.route("/<job_id>/unsave", methods=["DELETE"])
@auth_required(allowed_roles=["candidate"])
def unsave_job_route(job_id):
    candidate_id = request.user.get("id")

    remove_saved_job(candidate_id, job_id)

    return jsonify({"message": "Job removed from saved list"}), 200


@saved_job_bp.route("/saved", methods=["GET"])
@auth_required(allowed_roles=["candidate"])
def get_saved_jobs_route():
    candidate_id = request.user.get("id")

    jobs = get_saved_jobs(candidate_id)

    return jsonify({
        "count": len(jobs),
        "jobs": jobs
    }), 200
