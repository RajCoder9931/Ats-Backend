from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.interview_feedback_model import (
    create_interview_feedback,
    get_active_feedbacks,
    get_inactive_feedbacks,
    get_feedback_by_id,
    deactivate_feedback,
    activate_feedback
)

interview_feedback_bp = Blueprint(
    "interview_feedbacks",
    __name__,
    url_prefix="/api/interview-feedbacks"
)



@interview_feedback_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_interview_feedback():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required_fields = [
        "candidateId",
        "jobPostingId",
        "pipelineId",
        "interviewRound",
        "feedback",
        "result"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    data["createdBy"] = request.user.get("id")

    feedback = create_interview_feedback(data)

    if not feedback:
        return jsonify({"message": "Failed to create interview feedback"}), 500

    return jsonify(feedback), 201



@interview_feedback_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_feedbacks():
    feedbacks = get_active_feedbacks()
    return jsonify(feedbacks), 200



@interview_feedback_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_feedbacks():
    feedbacks = get_inactive_feedbacks()
    return jsonify(feedbacks), 200



@interview_feedback_bp.route("/<feedback_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_feedback_by_id(feedback_id):
    feedback = get_feedback_by_id(feedback_id)

    if not feedback:
        return jsonify({"message": "Interview feedback not found"}), 404

    return jsonify(feedback), 200



@interview_feedback_bp.route("/deactivate/<feedback_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(feedback_id):
    success = deactivate_feedback(feedback_id)

    if not success:
        return jsonify({"message": "Interview feedback not found"}), 404

    return jsonify({"message": "Interview feedback deactivated successfully"}), 200



@interview_feedback_bp.route("/activate/<feedback_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(feedback_id):
    success = activate_feedback(feedback_id)

    if not success:
        return jsonify({"message": "Interview feedback not found"}), 404

    return jsonify({"message": "Interview feedback activated successfully"}), 200
