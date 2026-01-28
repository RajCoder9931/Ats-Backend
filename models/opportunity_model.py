from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
opportunities = db.opportunities


def create_opportunity(data):
    now = datetime.datetime.utcnow()

    opp = {
        "leadId": ObjectId(data.get("leadId")),
        "companyName": data.get("companyName"),

        "jobTitle": data.get("jobTitle"),
        "jobCode": data.get("jobCode"),
        "jobDescription": data.get("jobDescription"),
        "department": data.get("department"),

        "employmentType": data.get("employmentType", "Full-time"),
        "experienceRequired": data.get("experienceRequired"),
        "skillsRequired": data.get("skillsRequired", []),
        "educationRequired": data.get("educationRequired"),
        "numberOfOpenings": data.get("numberOfOpenings"),

        "jobLocation": {
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country")
        },

        "workMode": data.get("workMode", "Onsite"),

        "salaryRange": {
            "min": data.get("salaryMin"),
            "max": data.get("salaryMax")
        },

        "incentiveType": data.get("incentiveType"),
        "incentiveAmount": data.get("incentiveAmount"),
        "paymentTerms": data.get("paymentTerms"),

        "contractStartDate": data.get("contractStartDate"),
        "contractEndDate": data.get("contractEndDate"),

        "opportunityStatus": data.get("opportunityStatus", "Open"),
        "priority": data.get("priority", "Medium"),
        "pipelineStage": data.get("pipelineStage", "Sourcing"),

        "closingDate": data.get("closingDate"),
        "remarks": data.get("remarks"),

        "isActive": True,
        "createdBy": data.get("createdBy"),

        "createdAt": now,
        "updatedAt": now
    }

    result = opportunities.insert_one(opp)

    opp["_id"] = str(result.inserted_id)
    opp["leadId"] = str(opp["leadId"])

    return opp


def get_active_opportunities():
    cursor = opportunities.find({
        "isActive": True
    }).sort("createdAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["leadId"] = str(doc["leadId"])
        result.append(doc)

    return result


def get_inactive_opportunities():
    cursor = opportunities.find({
        "isActive": False
    }).sort("updatedAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["leadId"] = str(doc["leadId"])
        result.append(doc)

    return result


def get_opportunity_by_id(opp_id):
    try:
        opp = opportunities.find_one({
            "_id": ObjectId(opp_id)
        })

        if not opp:
            return None

        opp["_id"] = str(opp["_id"])
        opp["leadId"] = str(opp["leadId"])
        return opp

    except Exception:
        return None


def deactivate_opportunity(opp_id):
    result = opportunities.update_one(
        {"_id": ObjectId(opp_id)},
        {"$set": {
            "isActive": False,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def activate_opportunity(opp_id):
    result = opportunities.update_one(
        {"_id": ObjectId(opp_id)},
        {"$set": {
            "isActive": True,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0
