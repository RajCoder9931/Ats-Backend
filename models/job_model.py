from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
jobs = db.jobs


def create_job(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = jobs.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_jobs():
    cursor = jobs.find().sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_jobs_for_candidate():
    cursor = jobs.find(
        {"status": "Active"},
        {
            "title": 1,
            "department": 1,
            "location": 1,
            "type": 1,
            "salaryRange": 1,
            "createdAt": 1
        }
    ).sort("createdAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_job_by_id(job_id):
    try:
        job = jobs.find_one({"_id": ObjectId(job_id)}, {"title": 1})
        return job
    except Exception:
        return None
