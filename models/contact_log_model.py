from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
contact_logs = db.contact_logs


def _serialize_log(doc):
    doc["_id"] = str(doc["_id"])
    if doc.get("leadId"):
        doc["leadId"] = str(doc["leadId"])
    if doc.get("contractId"):
        doc["contractId"] = str(doc["contractId"])
    return doc


def create_contact_log(data):
    now = datetime.datetime.utcnow()

    try:
        log = {
            "leadId": ObjectId(data.get("leadId")) if data.get("leadId") else None,
            "contractId": ObjectId(data.get("contractId")) if data.get("contractId") else None,

            "contactPerson": {
                "name": data.get("contactName"),
                "email": data.get("contactEmail"),
                "phone": data.get("contactPhone")
            },

            "communicationType": data.get("communicationType"),
            "subject": data.get("subject"),
            "description": data.get("description"),

            "outcome": data.get("outcome", "Pending"),
            "nextFollowUpDate": data.get("nextFollowUpDate"),

            "isActive": True,
            "createdBy": data.get("createdBy"),

            "createdAt": now,
            "updatedAt": now
        }

        result = contact_logs.insert_one(log)
        log["_id"] = str(result.inserted_id)

        return _serialize_log(log)

    except Exception as e:
        print("Create Contact Log Error:", e)
        return None


def get_active_logs():
    cursor = contact_logs.find({"isActive": True}).sort("createdAt", -1)
    return [_serialize_log(doc) for doc in cursor]


def get_inactive_logs():
    cursor = contact_logs.find({"isActive": False}).sort("updatedAt", -1)
    return [_serialize_log(doc) for doc in cursor]


def get_log_by_id(log_id):
    try:
        log = contact_logs.find_one({"_id": ObjectId(log_id)})
        if not log:
            return None
        return _serialize_log(log)
    except Exception:
        return None


def deactivate_log(log_id):
    try:
        result = contact_logs.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": {
                "isActive": False,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False


def activate_log(log_id):
    try:
        result = contact_logs.update_one(
            {"_id": ObjectId(log_id)},
            {"$set": {
                "isActive": True,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False
