from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.candidate_model import (
    create_candidate,
    get_all_candidates,
    update_candidate_by_id,
    get_candidate_by_id
)

from models.notification_model import create_notification

candidate_bp = Blueprint(
    "candidates",
    __name__,
    url_prefix="/api/candidates"
)


@candidate_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin"])
def add_candidate():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON body"}), 400

    required_fields = ["name", "email", "phone", "location", "source"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    candidate = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "location": data.get("location"),
        "country": data.get("country"),
        "state": data.get("state"),
        "locality": data.get("locality"),
        "dateOfBirth": data.get("dateOfBirth"),
        "gender": data.get("gender"),
        "skills": data.get("skills", []),
        "experience": data.get("experience", []),
        "education": data.get("education", []),
        "currentCompany": data.get("currentCompany"),
        "currentPosition": data.get("currentPosition"),
        "notes": data.get("notes"),
        "source": data.get("source"),
        "status": data.get("status", "Active"),
        "stage": "Applied",
        "createdBy": request.user.get("id"),
    }

    saved = create_candidate(candidate)

    create_notification({
        "userId": request.user.get("id"),
        "type": "candidate",
        "title": "New Candidate Added",
        "message": f"{candidate.get('name')} was added as a candidate",
        "entityId": saved.get("_id")
    })

    return jsonify(saved), 201


@candidate_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def fetch_candidates():
    return jsonify(get_all_candidates()), 200


@candidate_bp.route("/<candidate_id>", methods=["PUT"])
@auth_required(allowed_roles=["admin", "super_admin"])
def update_candidate(candidate_id):
    data = request.get_json()

    updated = update_candidate_by_id(candidate_id, data)

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    return jsonify(updated), 200
