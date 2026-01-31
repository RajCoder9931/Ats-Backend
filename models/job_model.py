from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

job_postings = db.job_postings
opportunities = db.opportunities


# -----------------------------
# CREATE FROM OPPORTUNITY
# -----------------------------
def create_job_posting_from_opportunity(opportunity_id, created_by):
    try:
        opportunity = opportunities.find_one({
            "_id": ObjectId(opportunity_id),
            "isActive": True
        })

        if not opportunity:
            return None

        
        existing = job_postings.find_one({
            "opportunityId": ObjectId(opportunity_id)
        })
        if existing:
            return "EXISTS"

        now = datetime.datetime.utcnow()

        job = {
            "opportunityId": opportunity.get("_id"),
            "companyName": opportunity.get("companyName"),

            "jobTitle": opportunity.get("jobTitle"),
            "jobSummary": opportunity.get("jobDescription"),
            "jobDescription": opportunity.get("jobDescription"),
            "department": opportunity.get("department"),

            "employmentType": opportunity.get("employmentType", "Full-time"),
            "workMode": opportunity.get("workMode", "Onsite"),

            "jobLocation": opportunity.get("jobLocation", {}),
            "numberOfOpenings": opportunity.get("numberOfOpenings"),

            "experienceRequired": opportunity.get("experienceRequired"),
            "skillsRequired": opportunity.get("skillsRequired", []),
            "educationRequired": opportunity.get("educationRequired"),

            "salaryRange": opportunity.get("salaryRange", {
                "min": None,
                "max": None
            }),

            "benefits": [],
            "applicationDeadline": None,

            "jobStatus": "Published",

            "totalApplications": 0,
            "shortlistedCount": 0,
            "hiredCount": 0,

            "isFeatured": False,
            "tags": [],

            "isActive": True,
            "createdBy": created_by,

            "createdAt": now,
            "updatedAt": now,
            "publishedAt": now
        }

        result = job_postings.insert_one(job)

        job["_id"] = str(result.inserted_id)
        job["opportunityId"] = str(job["opportunityId"])

        return job

    except Exception:
        return None


# -----------------------------
# FETCH APIS
# -----------------------------
def get_all_job_postings():
    cursor = job_postings.find().sort("createdAt", -1)
    result = []

    for job in cursor:
        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        result.append(job)

    return result


def get_active_job_postings():
    cursor = job_postings.find({
        "isActive": True
    }).sort("createdAt", -1)

    result = []
    for job in cursor:
        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        result.append(job)

    return result


def get_inactive_job_postings():
    cursor = job_postings.find({
        "isActive": False
    }).sort("updatedAt", -1)

    result = []
    for job in cursor:
        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        result.append(job)

    return result


def get_job_posting_by_id(job_id):
    try:
        job = job_postings.find_one({"_id": ObjectId(job_id)})
        if not job:
            return None

        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        return job

    except Exception:
        return None


def get_job_posting_by_opportunity_id(opportunity_id):
    try:
        job = job_postings.find_one({
            "opportunityId": ObjectId(opportunity_id)
        })

        if not job:
            return None

        job["_id"] = str(job["_id"])
        job["opportunityId"] = str(job["opportunityId"])
        return job

    except Exception:
        return None
