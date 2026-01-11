# from flask import Blueprint, request, jsonify
# from middleware.auth_middleware import auth_required
# from models.candidate_model import (
#     create_candidate,
#     get_all_candidates,
#     update_candidate_by_id
# )

# candidate_bp = Blueprint("candidates", __name__, url_prefix="/api/candidates")


# @candidate_bp.route("", methods=["POST"])
# @auth_required
# def add_candidate():
#     data = request.get_json()

#     if not data:
#         return jsonify({"message": "Invalid or missing JSON body"}), 400

#     required_fields = ["name", "email", "phone", "location", "source"]
#     for field in required_fields:
#         if not data.get(field):
#             return jsonify({"message": "{} is required".format(field)}), 400

#     candidate = {
#         "name": data.get("name"),
#         "email": data.get("email"),
#         "phone": data.get("phone"),
#         "location": data.get("location"),
#         "country": data.get("country"),
#         "state": data.get("state"),
#         "locality": data.get("locality"),
#         "dateOfBirth": data.get("dateOfBirth"),
#         "gender": data.get("gender"),
#         "skills": data.get("skills", []),    
#         "currentCompany": data.get("currentCompany"),
#         "currentPosition": data.get("currentPosition"),
#         "experience": data.get("experience"),
#         "notes": data.get("notes"),
#         "source": data.get("source"),
#         "status": "Active",
#         "stage": "Applied",
#         "createdBy": request.user.get("id"),
#     }

#     saved = create_candidate(candidate)
#     return jsonify(saved), 201

# @candidate_bp.route("", methods=["GET"])
# @auth_required
# def fetch_candidates():
#     data = get_all_candidates()
#     return jsonify(data), 200

# @candidate_bp.route("/<candidate_id>", methods=["PUT"])
# @auth_required
# def update_candidate(candidate_id):
#     data = request.get_json()

#     if not data:
#         return jsonify({"message": "Invalid JSON body"}), 400

#     updated = update_candidate_by_id(candidate_id, data)

#     if not updated:
#         return jsonify({"message": "Candidate not found"}), 404

#     updated["_id"] = str(updated["_id"])
#     return jsonify(updated), 200


##

from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.candidate_model import (
    create_candidate,
    get_all_candidates,
    update_candidate_by_id
)

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

    if not data:
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
    return jsonify(saved), 201


@candidate_bp.route("", methods=["GET"])
@auth_required
def fetch_candidates():
    data = get_all_candidates()
    return jsonify(data), 200

 
@candidate_bp.route("/<candidate_id>", methods=["PUT"])
@auth_required
def update_candidate(candidate_id):
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    updated = update_candidate_by_id(candidate_id, data)

    if not updated:
        return jsonify({"message": "Candidate not found"}), 404

    updated["_id"] = str(updated["_id"])
    return jsonify(updated), 200



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
    return jsonify(updated), 200
 
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
    return jsonify(updated), 200

 
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
    return jsonify(updated), 200
