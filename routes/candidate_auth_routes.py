from flask import Blueprint, request, jsonify
from utils.jwt_utils import generate_candidate_token
from utils.password_utils import hash_password, check_password
from models.candidate_profile_model import (
    find_candidate_by_email_and_role,
    create_candidate_profile
)

candidate_auth_bp = Blueprint(
    "candidate_auth",
    __name__,
    url_prefix="/api/candidate/auth"
)


@candidate_auth_bp.route("/signup", methods=["POST"])
def candidate_signup():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if find_candidate_by_email_and_role(data["email"]):
        return jsonify({"message": "Candidate already exists"}), 409

    candidate = {
        "name": data.get("name"),
        "email": data.get("email"),
        "password": hash_password(data.get("password")),
        "phone": data.get("phone"),
        "role": "candidate",
        "profile_completed": False
    }

    create_candidate_profile(candidate)

    return jsonify({"message": "Candidate registered successfully"}), 201


@candidate_auth_bp.route("/login", methods=["POST"])
def candidate_login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON body"}), 400

    candidate = find_candidate_by_email_and_role(data.get("email"))

    if not candidate or not check_password(
        data.get("password"), candidate["password"]
    ):
        return jsonify({"message": "Invalid credentials"}), 401

    token = generate_candidate_token(candidate)

    return jsonify({
        "candidate_token": token,
        "candidate": {
            "id": str(candidate["_id"]),
            "name": candidate["name"],
            "email": candidate["email"]
        }
    }), 200
