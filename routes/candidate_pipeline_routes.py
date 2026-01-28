from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.candidate_pipeline_model import (
    create_candidate_pipeline,
    get_active_pipelines,
    get_inactive_pipelines,
    get_pipeline_by_id,
    deactivate_pipeline,
    activate_pipeline
)

candidate_pipeline_bp = Blueprint("candidate_pipelines", __name__, url_prefix="/api/candidate-pipelines")

@candidate_pipeline_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def add_candidate_pipeline():
    data = request.get_json()

    required_fields = ["candidateId", "jobPostingId"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

    data["createdBy"] = request.user.get("id")

    pipeline = create_candidate_pipeline(data)
    return jsonify(pipeline), 201

@candidate_pipeline_bp.route("/active", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_active_pipelines():
    pipelines = get_active_pipelines()
    return jsonify(pipelines), 200

@candidate_pipeline_bp.route("/inactive", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_inactive_pipelines():
    pipelines = get_inactive_pipelines()
    return jsonify(pipelines), 200

@candidate_pipeline_bp.route("/<pipeline_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def fetch_pipeline_by_id(pipeline_id):
    pipeline = get_pipeline_by_id(pipeline_id)

    if not pipeline:
        return jsonify({"message": "Candidate pipeline not found"}), 404

    return jsonify(pipeline), 200

@candidate_pipeline_bp.route("/deactivate/<pipeline_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def deactivate(pipeline_id):
    success = deactivate_pipeline(pipeline_id)

    if not success:
        return jsonify({"message": "Candidate pipeline not found"}), 404

    return jsonify({"message": "Candidate pipeline deactivated successfully"}), 200

@candidate_pipeline_bp.route("/activate/<pipeline_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin", "recruiter"])
def activate(pipeline_id):
    success = activate_pipeline(pipeline_id)

    if not success:
        return jsonify({"message": "Candidate pipeline not found"}), 404

    return jsonify({"message": "Candidate pipeline activated successfully"}), 200
