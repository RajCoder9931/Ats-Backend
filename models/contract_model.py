from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

contracts = db.contracts
leads = db.leads


def create_contract_from_lead(lead_id, created_by):
    try:
        # Check if lead exists
        lead = leads.find_one({"_id": ObjectId(lead_id)})
        if not lead:
            return None, "Lead not found"

        # Prevent duplicate contract
        existing_contract = contracts.find_one({"leadId": ObjectId(lead_id)})
        if existing_contract:
            return None, "Contract already exists for this lead"

        now = datetime.datetime.utcnow()

        contract = {
            "leadId": ObjectId(lead_id),

            "companyName": lead.get("companyName"),
            "companyOwnerName": lead.get("companyOwnerName"),
            "companyEmail": lead.get("companyEmail"),
            "companyPhone": lead.get("companyPhone"),

            "industry": lead.get("industry"),
            "location": lead.get("location"),

            "contactPerson": lead.get("contactPerson"),

            "contractStatus": "Active",
            "startDate": now,
            "endDate": None,

            "remarks": lead.get("remarks"),

            "createdBy": created_by,
            "createdAt": now,
            "updatedAt": now
        }

        result = contracts.insert_one(contract)

        # Update lead status to Converted
        leads.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {
                "leadStatus": "Converted",
                "updatedAt": now
            }}
        )

        contract["_id"] = str(result.inserted_id)
        contract["leadId"] = str(contract["leadId"])

        return contract, None

    except Exception as e:
        print("Create Contract Error:", e)
        return None, str(e)


def _serialize_contract(doc):
    doc["_id"] = str(doc["_id"])
    if doc.get("leadId"):
        doc["leadId"] = str(doc["leadId"])
    return doc


def get_all_contracts():
    cursor = contracts.find().sort("createdAt", -1)
    return [_serialize_contract(doc) for doc in cursor]


def get_contract_by_id(contract_id):
    try:
        contract = contracts.find_one({"_id": ObjectId(contract_id)})
        if not contract:
            return None
        return _serialize_contract(contract)
    except Exception:
        return None


def deactivate_contract(contract_id):
    try:
        result = contracts.update_one(
            {"_id": ObjectId(contract_id)},
            {"$set": {
                "contractStatus": "Inactive",
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False
