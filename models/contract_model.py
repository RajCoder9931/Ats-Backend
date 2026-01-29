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
        existing_contract = contracts.find_one({"leadId": lead_id})
        if existing_contract:
            return None, "Contract already exists for this lead"

        now = datetime.datetime.utcnow()

        contract = {
            "leadId": lead_id,

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
        return contract, None

    except Exception as e:
        return None, str(e)


def get_all_contracts():
    cursor = contracts.find().sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_contract_by_id(contract_id):
    try:
        contract = contracts.find_one({"_id": ObjectId(contract_id)})

        if not contract:
            return None

        contract["_id"] = str(contract["_id"])
        return contract

    except Exception:
        return None


def deactivate_contract(contract_id):
    result = contracts.update_one(
        {"_id": ObjectId(contract_id)},
        {"$set": {
            "contractStatus": "Inactive",
            "updatedAt": datetime.datetime.utcnow()
        }}
    )

    return result.modified_count > 0
