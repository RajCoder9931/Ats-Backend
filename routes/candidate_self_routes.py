from flask import Blueprint, request, jsonify
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
# Get Own Profile
# ==========================
@candidate_self_bp.route("/me", methods=["GET"])
@auth_required(allowed_roles=["candidate"])
def get_my_profile():
    candidate = find_candidate_profile_by_id(request.user["id"])

    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    candidate["_id"] = str(candidate["_id"])
    candidate.pop("password", None)

    return jsonify(candidate), 200


# ==========================
# Update Own Profile (FULL PROFILE)
# ==========================
@candidate_self_bp.route("/me", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def update_my_profile():
    data = request.json

    
    allowed_fields = [
        # Basic info
        "name",
        "phone",
        "dateOfBirth",
        "gender",

        # Location
        "location",          # {country, state, city, pincode}

        # Skills & work
        "skills",            # []
        "experience",        # []
        "education",         # []
        "certifications",    # []
        "projects",          # []

        # Links
        "resume_url",
        "portfolio_url",
        "linkedin_url",
        "github_url",

        # Preferences
        "preferred_job_roles",
        "preferred_locations",
        "expected_salary",   # {currency, amount}
        "notice_period_days",
        "willing_to_relocate",

        # Languages
        "languages",         # [{language, proficiency}]

        # Meta
        "profile_completed"
    ]

    update_data = {
        field: data[field]
        for field in allowed_fields
        if field in data
    }

    if not update_data:
        return jsonify({"message": "Nothing to update"}), 400

    candidate = update_candidate_profile(
        request.user["id"],
        update_data
    )

    candidate["_id"] = str(candidate["_id"])
    candidate.pop("password", None)

    return jsonify(candidate), 200


# ==========================
# Change Password
# ==========================
@candidate_self_bp.route("/change-password", methods=["PUT"])
@auth_required(allowed_roles=["candidate"])
def change_candidate_password():
    data = request.json

    current_password = data.get("currentPassword")
    new_password = data.get("newPassword")

    if not current_password or not new_password:
        return jsonify({"message": "All fields required"}), 400

    candidate = find_candidate_profile_by_id(request.user["id"])

    if not check_password(current_password, candidate["password"]):
        return jsonify({"message": "Current password incorrect"}), 401

    update_candidate_profile(
        request.user["id"],
        {"password": hash_password(new_password)}
    )

    return jsonify({"message": "Password updated successfully"}), 200
