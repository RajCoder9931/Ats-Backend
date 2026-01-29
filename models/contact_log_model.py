from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
contact_logs = db.contact_logs


def create_contact_log(data):
    now = datetime.datetime.utcnow()

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
    if log["leadId"]:
        log["leadId"] = str(log["leadId"])
    if log["contractId"]:
        log["contractId"] = str(log["contractId"])

    return log


def get_active_logs():
    cursor = contact_logs.find({"isActive": True}).sort("createdAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if doc.get("leadId"):
            doc["leadId"] = str(doc["leadId"])
        if doc.get("contractId"):
            doc["contractId"] = str(doc["contractId"])
        result.append(doc)

    return result


def get_inactive_logs():
    cursor = contact_logs.find({"isActive": False}).sort("updatedAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if doc.get("leadId"):
            doc["leadId"] = str(doc["leadId"])
        if doc.get("contractId"):
            doc["contractId"] = str(doc["contractId"])
        result.append(doc)

    return result


def get_log_by_id(log_id):
    try:
        log = contact_logs.find_one({"_id": ObjectId(log_id)})

        if not log:
            return None

        log["_id"] = str(log["_id"])
        if log.get("leadId"):
            log["leadId"] = str(log["leadId"])
        if log.get("contractId"):
            log["contractId"] = str(log["contractId"])

        return log

    except Exception:
        return None


def deactivate_log(log_id):
    result = contact_logs.update_one(
        {"_id": ObjectId(log_id)},
        {"$set": {
            "isActive": False,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def activate_log(log_id):
    result = contact_logs.update_one(
        {"_id": ObjectId(log_id)},
        {"$set": {
            "isActive": True,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0
