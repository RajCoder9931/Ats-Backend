from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.job_model import create_job, get_all_jobs

job_bp = Blueprint("jobs", __name__, url_prefix="/api/jobs")


@job_bp.route("", methods=["POST"])
@auth_required
def add_job():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

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
            return jsonify({
                "message": "{} is required".format(field)
            }), 400

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
    return jsonify(saved), 201


@job_bp.route("", methods=["GET"])
@auth_required
def fetch_jobs():
    data = get_all_jobs()
    return jsonify(data), 200

