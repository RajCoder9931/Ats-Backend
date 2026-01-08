# routes/company_routes.py
from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.company_model import (
    create_company,
    get_all_companies,
    get_company_by_id
)

company_bp = Blueprint("companies", __name__, url_prefix="/api/companies")


@company_bp.route("", methods=["POST"])
@auth_required
def add_company():
    data = request.json

    required_fields = [
        "name",
        "industry",
        "website",
        "location",
        "email",
        "owner",
        "currency",
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "message": "{} is required".format(field)
            }), 400

    company = {
        "name": data.get("name"),
        "industry": data.get("industry"),
        "website": data.get("website"),
        "location": data.get("location"),
        "size": data.get("size"),
        "contactPerson": data.get("contactPerson"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "notes": data.get("notes"),
        "owner": data.get("owner"),
        "currency": data.get("currency"),
        "createdBy": request.user.get("id"),
    }

    saved = create_company(company)
    return jsonify(saved), 201


@company_bp.route("", methods=["GET"])
@auth_required
def fetch_companies():
    data = get_all_companies()
    return jsonify(data), 200


@company_bp.route("/<company_id>", methods=["GET"])
@auth_required
def fetch_company(company_id):
    company = get_company_by_id(company_id)
    if not company:
        return jsonify({"message": "Company not found"}), 404
    return jsonify(company), 200
