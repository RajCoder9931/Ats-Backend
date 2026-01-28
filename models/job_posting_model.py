from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
job_postings = db.job_postings


def create_job_posting(data):
    now = datetime.datetime.utcnow()

    job = {
        "opportunityId": ObjectId(data.get("opportunityId")),
        "companyName": data.get("companyName"),

        "jobTitle": data.get("jobTitle"),
        "jobSummary": data.get("jobSummary"),
        "jobDescription": data.get("jobDescription"),
        "department": data.get("department"),

        "employmentType": data.get("employmentType", "Full-time"),
        "workMode": data.get("workMode", "Onsite"),

        "jobLocation": {
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country")
        },

        "numberOfOpenings": data.get("numberOfOpenings"),

        "experienceRequired": data.get("experienceRequired"),
        "skillsRequired": data.get("skillsRequired", []),
        "educationRequired": data.get("educationRequired"),

        "salaryRange": {
            "min": data.get("salaryMin"),
            "max": data.get("salaryMax")
        },

        "benefits": data.get("benefits", []),

        "applicationDeadline": data.get("applicationDeadline"),
        "maxApplications": data.get("maxApplications"),
        "allowMultipleApplications": data.get("allowMultipleApplications", False),
        "autoCloseWhenFilled": data.get("autoCloseWhenFilled", True),

        "jobStatus": data.get("jobStatus", "Draft"),
        "totalApplications": 0,
        "shortlistedCount": 0,
        "hiredCount": 0,

        "isFeatured": data.get("isFeatured", False),
        "tags": data.get("tags", []),

        "isActive": True,
        "createdBy": data.get("createdBy"),

        "createdAt": now,
        "updatedAt": now,
        "publishedAt": None
    }

    result = job_postings.insert_one(job)

    job["_id"] = str(result.inserted_id)
    job["opportunityId"] = str(job["opportunityId"])

    return job


def get_active_job_postings():
    cursor = job_postings.find({
        "isActive": True
    }).sort("createdAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["opportunityId"] = str(doc["opportunityId"])
        result.append(doc)

    return result


def get_inactive_job_postings():
    cursor = job_postings.find({
        "isActive": False
    }).sort("updatedAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["opportunityId"] = str(doc["opportunityId"])
        result.append(doc)

    return result


def get_job_posting_by_id(job_id):
    try:
        job = job_postings.find_one({
            "_id": ObjectId(job_id)
        })

        if not job:
            return None

        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        return job

    except Exception:
        return None


def deactivate_job_posting(job_id):
    result = job_postings.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {
            "isActive": False,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def activate_job_posting(job_id):
    result = job_postings.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {
            "isActive": True,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0
