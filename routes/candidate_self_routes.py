from flask import Blueprint, request, jsonify
from bson import ObjectId
from middleware.auth_middleware import auth_required
from utils.password_utils import check_password, hash_password
from models.candidate_profile_model import (
    find_candidate_profile_by_id,
    update_candidate_profile
)

candidate_self_bp = Blueprint(
    "candidate_self",
    __name__,
    url_prefix="/api/candidate"
)


# ==========================
# Serializer
# ==========================
def serialize(obj):
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


# ==========================
# GET MY PROFILE
# ==========================
@candidate_self_bp.route("/me", methods=["GET"])
@auth_required(allowed_roles=["candidate"])
def get_my_profile():
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    candidate = serialize(candidate)
    candidate.pop("password", None)

    return jsonify(candidate), 200


# ==========================
# UPDATE PROFILE
# ==========================
@candidate_self_bp.route("/me", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def update_my_profile():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid JSON body"}), 400

    allowed_fields = [
        "name", "phone", "dateOfBirth", "gender",
        "location",
        "skills",
        "certifications", "projects",
        "resume_url", "portfolio_url", "linkedin_url", "github_url",
        "preferred_job_roles", "preferred_locations",
        "expected_salary", "notice_period_days", "willing_to_relocate",
        "languages",
        "profile_completed"
    ]

    update_data = {field: data[field] for field in allowed_fields if field in data}

    if not update_data:
        return jsonify({"message": "Nothing to update"}), 400

    candidate = update_candidate_profile(request.user["id"], update_data)

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    candidate = serialize(candidate)
    candidate.pop("password", None)

    return jsonify(candidate), 200


# ==========================
# EXPERIENCE CRUD
# ==========================
@candidate_self_bp.route("/experience", methods=["POST"])
@auth_required(allowed_roles=["candidate"])
def add_experience():
    data = request.get_json()

    if not data or not data.get("company") or not data.get("role"):
        return jsonify({"message": "Company and role required"}), 400

    experience = {
        "_id": ObjectId(),
        "company": data.get("company"),
        "role": data.get("role"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "description": data.get("description")
    }

    candidate = find_candidate_profile_by_id(request.user["id"])
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    experiences = candidate.get("experience", [])
    experiences.append(experience)

    update_candidate_profile(request.user["id"], {"experience": experiences})

    return jsonify(serialize(experience)), 201


@candidate_self_bp.route("/experience/<exp_id>", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def update_experience(exp_id):
    data = request.get_json()
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    experiences = candidate.get("experience", [])
    found = False

    for exp in experiences:
        if str(exp["_id"]) == exp_id:
            exp["company"] = data.get("company", exp.get("company"))
            exp["role"] = data.get("role", exp.get("role"))
            exp["start_date"] = data.get("start_date", exp.get("start_date"))
            exp["end_date"] = data.get("end_date", exp.get("end_date"))
            exp["description"] = data.get("description", exp.get("description"))
            found = True
            break

    if not found:
        return jsonify({"message": "Experience not found"}), 404

    update_candidate_profile(request.user["id"], {"experience": experiences})

    return jsonify({"message": "Experience updated successfully"}), 200


@candidate_self_bp.route("/experience/<exp_id>", methods=["DELETE"])
@auth_required(allowed_roles=["candidate"])
def delete_experience(exp_id):
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    experiences = candidate.get("experience", [])
    new_experiences = [e for e in experiences if str(e["_id"]) != exp_id]

    update_candidate_profile(request.user["id"], {"experience": new_experiences})

    return jsonify({"message": "Experience removed"}), 200


# ==========================
# EDUCATION CRUD
# ==========================
@candidate_self_bp.route("/education", methods=["POST"])
@auth_required(allowed_roles=["candidate"])
def add_education():
    data = request.get_json()

    if not data or not data.get("institution") or not data.get("degree"):
        return jsonify({"message": "Institution and degree required"}), 400

    education = {
        "_id": ObjectId(),
        "institution": data.get("institution"),
        "degree": data.get("degree"),
        "field_of_study": data.get("field_of_study"),
        "start_year": data.get("start_year"),
        "end_year": data.get("end_year"),
        "description": data.get("description")
    }

    candidate = find_candidate_profile_by_id(request.user["id"])
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    education_list = candidate.get("education", [])
    education_list.append(education)

    update_candidate_profile(request.user["id"], {"education": education_list})

    return jsonify(serialize(education)), 201


@candidate_self_bp.route("/education/<edu_id>", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def update_education(edu_id):
    data = request.get_json()
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    education_list = candidate.get("education", [])
    found = False

    for edu in education_list:
        if str(edu["_id"]) == edu_id:
            edu["institution"] = data.get("institution", edu.get("institution"))
            edu["degree"] = data.get("degree", edu.get("degree"))
            edu["field_of_study"] = data.get("field_of_study", edu.get("field_of_study"))
            edu["start_year"] = data.get("start_year", edu.get("start_year"))
            edu["end_year"] = data.get("end_year", edu.get("end_year"))
            edu["description"] = data.get("description", edu.get("description"))
            found = True
            break

    if not found:
        return jsonify({"message": "Education not found"}), 404

    update_candidate_profile(request.user["id"], {"education": education_list})

    return jsonify({"message": "Education updated successfully"}), 200


@candidate_self_bp.route("/education/<edu_id>", methods=["DELETE"])
@auth_required(allowed_roles=["candidate"])
def delete_education(edu_id):
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    education_list = candidate.get("education", [])
    new_education = [e for e in education_list if str(e["_id"]) != edu_id]

    update_candidate_profile(request.user["id"], {"education": new_education})

    return jsonify({"message": "Education removed"}), 200


# ==========================
# CHANGE PASSWORD
# ==========================
@candidate_self_bp.route("/change-password", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def change_candidate_password():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"message": "All fields required"}), 400

    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    if not check_password(current_password, candidate["password"]):
        return jsonify({"message": "Current password incorrect"}), 401

    update_candidate_profile(
        request.user["id"],
        {"password": hash_password(new_password)}
    )

    return jsonify({"message": "Password updated successfully"}), 200
