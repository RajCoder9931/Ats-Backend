from flask import Blueprint, request, jsonify
from middleware.auth_middleware import auth_required
from models.lead_model import create_lead, get_all_leads
from models.job_model import get_job_by_id
from models.candidate_model import get_candidate_by_id
from models.lead_model import create_lead, get_all_leads, get_lead_by_id

lead_bp = Blueprint("leads", __name__, url_prefix="/api/leads")



@lead_bp.route("", methods=["POST"])
@auth_required
def add_lead():
    data = request.get_json()

    required = ["name", "stage"]
    for field in required:
        if not data.get(field):
            return jsonify({"message": "{} is required".format(field)}), 400

    job = get_job_by_id(data.get("jobId")) if data.get("jobId") else None
    candidate = get_candidate_by_id(data.get("candidateId")) if data.get("candidateId") else None

    lead = {
        "name": data.get("name"),
        "stage": data.get("stage"),
        "expectedValue": data.get("expectedValue"),
        "followUpDate": data.get("followUpDate"),

        "companyId": data.get("companyId"),
        "companyName": data.get("companyName"),

        "contactId": data.get("contactId"),
        "contactName": data.get("contactName"),

        "jobId": data.get("jobId"),
        "jobTitle": job.get("title") if job else None,

        "candidateId": data.get("candidateId"),
        "candidateName": candidate.get("name") if candidate else None,

        "createdBy": request.user.get("id")
    }

    saved = create_lead(lead)
    return jsonify(saved), 201
 
@lead_bp.route("", methods=["GET"])
@auth_required
def fetch_leads():
    data = get_all_leads(request.user.get("id"))
    return jsonify(data), 200

@lead_bp.route("/<lead_id>", methods=["GET"])
@auth_required
def fetch_lead_by_id(lead_id):
    lead = get_lead_by_id(lead_id, request.user.get("id"))

    if not lead:
        return jsonify({"message": "Lead not found"}), 404

    return jsonify(lead), 200
