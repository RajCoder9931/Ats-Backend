from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
leads = db.leads


def _serialize_lead(doc):
    doc["_id"] = str(doc["_id"])
    return doc


def create_lead(data):
    now = datetime.datetime.utcnow()

    try:
        lead = {
            "companyName": data.get("companyName"),
            "companyOwnerName": data.get("companyOwnerName"),
            "companyEmail": data.get("companyEmail"),
            "companyPhone": data.get("companyPhone"),

            "industry": data.get("industry"),
            "companySize": data.get("companySize"),
            "website": data.get("website"),

            "location": {
                "city": data.get("city"),
                "state": data.get("state"),
                "country": data.get("country")
            },

            "contactPerson": {
                "name": data.get("contactName"),
                "email": data.get("contactEmail"),
                "phone": data.get("contactPhone"),
                "designation": data.get("contactDesignation")
            },

            "leadSource": data.get("leadSource"),
            "leadStatus": data.get("leadStatus", "New"),
            "priority": data.get("priority", "Medium"),
            "expectedHiring": data.get("expectedHiring", False),
            "remarks": data.get("remarks"),

            "isActive": True,
            "createdBy": data.get("createdBy"),

            "createdAt": now,
            "updatedAt": now,
            "lastContactedAt": None
        }

        result = leads.insert_one(lead)
        lead["_id"] = str(result.inserted_id)

        return lead

    except Exception as e:
        print("Create Lead Error:", e)
        return None


def get_active_leads():
    try:
        cursor = leads.find({"isActive": True}).sort("createdAt", -1)
        return [_serialize_lead(doc) for doc in cursor]
    except Exception as e:
        print("Get Active Leads Error:", e)
        return []


def get_inactive_leads():
    try:
        cursor = leads.find({"isActive": False}).sort("updatedAt", -1)
        return [_serialize_lead(doc) for doc in cursor]
    except Exception as e:
        print("Get Inactive Leads Error:", e)
        return []


def get_lead_by_id(lead_id):
    try:
        lead = leads.find_one({"_id": ObjectId(lead_id)})
        if not lead:
            return None
        return _serialize_lead(lead)
    except Exception:
        return None


def deactivate_lead(lead_id):
    try:
        result = leads.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {
                "isActive": False,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False


def activate_lead(lead_id):
    try:
        result = leads.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": {
                "isActive": True,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False


def update_lead(lead_id, data):
    try:
        update_data = {
            "companyName": data.get("companyName"),
            "companyOwnerName": data.get("companyOwnerName"),
            "companyEmail": data.get("companyEmail"),
            "companyPhone": data.get("companyPhone"),

            "industry": data.get("industry"),
            "companySize": data.get("companySize"),
            "website": data.get("website"),

            "location.city": data.get("city"),
            "location.state": data.get("state"),
            "location.country": data.get("country"),

            "contactPerson.name": data.get("contactName"),
            "contactPerson.email": data.get("contactEmail"),
            "contactPerson.phone": data.get("contactPhone"),
            "contactPerson.designation": data.get("contactDesignation"),

            "leadSource": data.get("leadSource"),
            "leadStatus": data.get("leadStatus"),
            "priority": data.get("priority"),
            "expectedHiring": data.get("expectedHiring"),
            "remarks": data.get("remarks"),

            "updatedAt": datetime.datetime.utcnow()
        }

        # remove None values
        clean_data = {k: v for k, v in update_data.items() if v is not None}

        result = leads.update_one(
            {"_id": ObjectId(lead_id)},
            {"$set": clean_data}
        )

        return result.modified_count > 0

    except Exception as e:
        print("Update Lead Error:", e)
        return False
