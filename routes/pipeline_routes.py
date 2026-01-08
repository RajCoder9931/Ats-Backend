from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.pipeline_model import (
    assign_job_to_candidate,
    update_candidate_stage
)

pipeline_bp = Blueprint(
    "pipeline",
    __name__,
    url_prefix="/api/pipeline"
)

@pipeline_bp.route("/assign", methods=["POST"])
@auth_required
def assign_job():
    data = request.json

    candidate_id = data.get("candidateId")
    job_id = data.get("jobId")
    job_title = data.get("jobTitle")

    if not all([candidate_id, job_id, job_title]):
        return jsonify({"message": "candidateId, jobId, jobTitle required"}), 400

    candidate = assign_job_to_candidate(candidate_id, job_id, job_title)

    candidate["_id"] = str(candidate["_id"])

    return jsonify({
        "message": "Job assigned successfully",
        "candidate": candidate
    }), 200


@pipeline_bp.route("/stage", methods=["PUT"])
@auth_required
def change_stage():
    data = request.json

    candidate_id = data.get("candidateId")
    stage = data.get("stage")

    if not candidate_id or not stage:
        return jsonify({"message": "candidateId and stage required"}), 400

    candidate = update_candidate_stage(candidate_id, stage)

    if not candidate:
        return jsonify({"message": "Invalid stage"}), 400

    candidate["_id"] = str(candidate["_id"])

    return jsonify({
        "message": "Stage updated successfully",
        "candidate": candidate
    }), 200
