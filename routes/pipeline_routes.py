from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.pipeline_model import (
    assign_job_to_candidate,
    update_candidate_stage,
    get_candidates_by_job,
    get_candidates_by_stage,
    get_candidate_pipeline
)

pipeline_bp = Blueprint(
    "pipeline",
    __name__,
    url_prefix="/api/pipeline"
)



@pipeline_bp.route("/assign", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin"])
def assign_job():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    candidate_id = data.get("candidateId")
    job_id = data.get("jobId")
    job_title = data.get("jobTitle")

    if not all([candidate_id, job_id, job_title]):
        return jsonify({"message": "candidateId, jobId and jobTitle are required"}), 400

    candidate = assign_job_to_candidate(candidate_id, job_id, job_title)

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    candidate["_id"] = str(candidate["_id"])

    return jsonify({
        "message": "Job assigned successfully",
        "candidate": candidate
    }), 200



@pipeline_bp.route("/stage", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin"])
def change_stage():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON body"}), 400

    candidate_id = data.get("candidateId")
    stage = data.get("stage")

    if not candidate_id or not stage:
        return jsonify({"message": "candidateId and stage are required"}), 400

    candidate = update_candidate_stage(candidate_id, stage)

    if not candidate:
        return jsonify({"message": "Invalid stage or candidate not found"}), 400

    candidate["_id"] = str(candidate["_id"])

    return jsonify({
        "message": "Stage updated successfully",
        "candidate": candidate
    }), 200



@pipeline_bp.route("/job/<job_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def candidates_by_job(job_id):
    candidates = get_candidates_by_job(job_id)

    for c in candidates:
        c["_id"] = str(c["_id"])

    return jsonify(candidates), 200



@pipeline_bp.route("/stage/<stage>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def candidates_by_stage(stage):
    candidates = get_candidates_by_stage(stage)

    for c in candidates:
        c["_id"] = str(c["_id"])

    return jsonify(candidates), 200



@pipeline_bp.route("/candidate/<candidate_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def candidate_pipeline(candidate_id):
    candidate = get_candidate_pipeline(candidate_id)

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    candidate["_id"] = str(candidate["_id"])

    return jsonify(candidate), 200
