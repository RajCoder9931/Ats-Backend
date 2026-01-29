from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
leads = db.leads


def create_lead(data):
    now = datetime.datetime.utcnow()

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


def get_active_leads():
    cursor = leads.find({"isActive": True}).sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_inactive_leads():
    cursor = leads.find({"isActive": False}).sort("updatedAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_lead_by_id(lead_id):
    try:
        lead = leads.find_one({"_id": ObjectId(lead_id)})

        if not lead:
            return None

        lead["_id"] = str(lead["_id"])
        return lead

    except Exception:
        return None


def deactivate_lead(lead_id):
    result = leads.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {
            "isActive": False,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def activate_lead(lead_id):
    result = leads.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": {
            "isActive": True,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def update_lead(lead_id, data):
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

    clean_data = {}
    for key in update_data:
        if update_data[key] is not None:
            clean_data[key] = update_data[key]

    result = leads.update_one(
        {"_id": ObjectId(lead_id)},
        {"$set": clean_data}
    )

    return result.modified_count > 0
