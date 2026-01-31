from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.company_model import (
    create_company,
    get_all_companies,
    get_company_by_id
)


company_bp = Blueprint(
    "companies",
    __name__,
    url_prefix="/api/companies"
)



@company_bp.route("", methods=["POST"])
@auth_required(allowed_roles=["admin", "super_admin"])
def add_company():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid or missing JSON body"}), 400

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
            return jsonify({"message": f"{field} is required"}), 400

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

    if not saved:
        return jsonify({"message": "Failed to create company"}), 500

    return jsonify(saved), 201



@company_bp.route("", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def fetch_companies():
    companies = get_all_companies()
    return jsonify(companies), 200



@company_bp.route("/<company_id>", methods=["GET"])
@auth_required(allowed_roles=["admin", "super_admin"])
def fetch_company(company_id):
    company = get_company_by_id(company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    return jsonify(company), 200
