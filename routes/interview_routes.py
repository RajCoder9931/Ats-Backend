from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required

from models.interview_model import create_interview, get_upcoming_interviews
from models.candidate_model import get_candidate_by_id
from models.job_model import get_job_by_id


interview_bp = Blueprint("interviews", __name__, url_prefix="/api/interviews")


@interview_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin"])
def schedule_interview():
    data = request.json

    required_fields = [
        "candidateId",
        "jobId",
        "type",
        "date",
        "time",
        "duration",
        "interviewer",
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": "{} is required".format(field)
            }), 400

     
    candidate = get_candidate_by_id(data["candidateId"])
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

     
    job = get_job_by_id(data["jobId"])
    if not job:
        return jsonify({"message": "Job not found"}), 404

    interview = {
        "candidateId": data["candidateId"],
        "candidateName": candidate["name"],    
        "jobId": data["jobId"],
        "jobTitle": job["title"],               
        "type": data["type"],
        "date": data["date"],
        "time": data["time"],
        "duration": data["duration"],
        "interviewer": data["interviewer"],
        "meetingLink": data.get("meetingLink"),
        "notes": data.get("notes"),
        "status": "Scheduled",
        "createdBy": request.user.get("id"),
    }

    saved = create_interview(interview)
    return jsonify(saved), 201


@interview_bp.route("/upcoming", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def upcoming_interviews():
    return jsonify(get_upcoming_interviews()), 200
