from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.job_model import (
    create_job,
    get_all_jobs,
    get_jobs_for_candidate
)

job_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/api/jobs"
)


@job_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin"])
def add_job():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required_fields = [
        "title",
        "department",
        "location",
        "type",
        "status",
        "salaryRange",
        "hiringManager",
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    job = {
        "title": data.get("title"),
        "department": data.get("department"),
        "location": data.get("location"),
        "type": data.get("type"),
        "status": data.get("status"),
        "salaryRange": data.get("salaryRange"),
        "hiringManager": data.get("hiringManager"),
        "applicants": 0,
        "createdBy": request.user.get("id"),
    }

    saved = create_job(job)

    if not saved:
        return jsonify({"message": "Failed to create job"}), 500

    return jsonify(saved), 201



@job_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "candidate"])
def fetch_jobs():
    role = request.user.get("role")

    if role == "candidate":
        jobs = get_jobs_for_candidate()
    else:
        jobs = get_all_jobs()

    return jsonify(jobs), 200
