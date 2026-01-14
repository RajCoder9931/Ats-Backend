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

# ================= CREATE CANDIDATE =================
@candidate_bp.route("", methods=["POST"])
@auth_required
def add_candidate():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required_fields = ["name", "email", "phone", "location", "source"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

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
        "message": "{} was added as a candidate".format(candidate.get("name")),
        "entityId": saved.get("_id")
    })

    return jsonify(saved), 201


# ================= GET ALL CANDIDATES =================
@candidate_bp.route("", methods=["GET"])
@auth_required
def fetch_candidates():
    return jsonify(get_all_candidates()), 200


# ================= UPDATE CANDIDATE =================
@candidate_bp.route("/<candidate_id>", methods=["PUT"])
@auth_required
def update_candidate(candidate_id):
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON body"}), 400

    updated = update_candidate_by_id(candidate_id, data)

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    updated["_id"] = str(updated["_id"])

    create_notification({
        "userId": request.user.get("id"),
        "type": "candidate",
        "title": "Candidate Updated",
        "message": "{} profile was updated".format(updated.get("name")),
        "entityId": updated["_id"]
    })

    return jsonify(updated), 200


# ================= UPDATE STATUS =================
@candidate_bp.route("/<candidate_id>/status", methods=["PUT"])
@auth_required
def update_candidate_status(candidate_id):
    data = request.get_json()
    status = data.get("status")

    if status not in ["Active", "Inactive"]:
        return jsonify({"message": "Status must be Active or Inactive"}), 400

    updated = update_candidate_by_id(candidate_id, {"status": status})

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    updated["_id"] = str(updated["_id"])

    create_notification({
        "userId": request.user.get("id"),
        "type": "candidate",
        "title": "Candidate Status Changed",
        "message": "{} marked as {}".format(updated.get("name"), status),
        "entityId": updated["_id"]
    })

    return jsonify(updated), 200


# ================= EXPERIENCE =================
@candidate_bp.route("/<candidate_id>/experience", methods=["PUT"])
@auth_required
def update_experience(candidate_id):
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "Experience must be an array"}), 400

    updated = update_candidate_by_id(candidate_id, {"experience": data})

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    updated["_id"] = str(updated["_id"])

    create_notification({
        "userId": request.user.get("id"),
        "type": "candidate",
        "title": "Experience Updated",
        "message": "Experience updated for {}".format(updated.get("name")),
        "entityId": updated["_id"]
    })

    return jsonify(updated), 200


@candidate_bp.route("/<candidate_id>/experience", methods=["GET"])
@auth_required
def fetch_experience(candidate_id):
    candidate = get_candidate_by_id(candidate_id)

    return jsonify({
        "candidateId": candidate_id,
        "experience": candidate.get("experience", []) if candidate else []
    }), 200


# ================= EDUCATION =================
@candidate_bp.route("/<candidate_id>/education", methods=["PUT"])
@auth_required
def update_education(candidate_id):
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"message": "Education must be an array"}), 400

    updated = update_candidate_by_id(candidate_id, {"education": data})

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    updated["_id"] = str(updated["_id"])

    create_notification({
        "userId": request.user.get("id"),
        "type": "candidate",
        "title": "Education Updated",
        "message": "Education updated for {}".format(updated.get("name")),
        "entityId": updated["_id"]
    })

    return jsonify(updated), 200


@candidate_bp.route("/<candidate_id>/education", methods=["GET"])
@auth_required
def fetch_education(candidate_id):
    candidate = get_candidate_by_id(candidate_id)

    return jsonify({
        "candidateId": candidate_id,
        "education": candidate.get("education", []) if candidate else []
    }), 200
