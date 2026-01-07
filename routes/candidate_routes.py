# routes/candidate_routes.py
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.candidate_model import create_candidate, get_all_candidates

candidate_bp = Blueprint("candidates", __name__, url_prefix="/api/candidates")


# ================= ADD CANDIDATE =================
@candidate_bp.route("", methods=["POST"])
@auth_required
def add_candidate():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    required_fields = ["name", "email", "phone", "location", "source"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": "{} is required".format(field)
            }), 400

    candidate = {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "location": data.get("location"),
        "currentCompany": data.get("currentCompany"),
        "currentPosition": data.get("currentPosition"),
        "experience": data.get("experience"),
        "notes": data.get("notes"),
        "source": data.get("source"),
        "status": "Active",
        "stage": "Applied",
        "createdBy": request.user.get("id"),
    }

    saved = create_candidate(candidate)
    return jsonify(saved), 201


# ================= FETCH CANDIDATES =================
@candidate_bp.route("", methods=["GET"])
@auth_required
def fetch_candidates():
    data = get_all_candidates()
    return jsonify(data), 200
