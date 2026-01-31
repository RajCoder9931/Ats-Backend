from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

saved_jobs = db.saved_jobs
jobs = db.jobs


def _serialize_saved_job(doc):
    doc["_id"] = str(doc["_id"])
    doc["candidateId"] = str(doc["candidateId"])
    doc["jobId"] = str(doc["jobId"])
    return doc


# ================= CHECK ALREADY SAVED =================
def is_job_saved(candidate_id, job_id):
    try:
        return saved_jobs.find_one({
            "candidateId": ObjectId(candidate_id),
            "jobId": ObjectId(job_id)
        })
    except Exception:
        return None


# ================= SAVE JOB =================
def save_job(candidate_id, job_id):
    try:
        data = {
            "candidateId": ObjectId(candidate_id),
            "jobId": ObjectId(job_id),
            "savedAt": datetime.datetime.utcnow()
        }

        result = saved_jobs.insert_one(data)
        data["_id"] = str(result.inserted_id)

        return _serialize_saved_job(data)

    except Exception as e:
        print("Save Job Error:", e)
        return None


# ================= REMOVE SAVED JOB =================
def remove_saved_job(candidate_id, job_id):
    try:
        saved_jobs.delete_one({
            "candidateId": ObjectId(candidate_id),
            "jobId": ObjectId(job_id)
        })
        return True
    except Exception:
        return False


# ================= GET SAVED JOBS =================
def get_saved_jobs(candidate_id):
    try:
        pipeline = [
            {
                "$match": {
                    "candidateId": ObjectId(candidate_id)
                }
            },
            {
                "$lookup": {
                    "from": "jobs",
                    "localField": "jobId",
                    "foreignField": "_id",
                    "as": "job"
                }
            },
            {"$unwind": "$job"},
            {"$sort": {"savedAt": -1}},
            {
                "$project": {
                    "_id": 1,
                    "savedAt": 1,
                    "job._id": 1,
                    "job.title": 1,
                    "job.department": 1,
                    "job.location": 1,
                    "job.type": 1,
                    "job.salaryRange": 1
                }
            }
        ]

        result = []
        for doc in saved_jobs.aggregate(pipeline):
            doc["_id"] = str(doc["_id"])
            doc["job"]["_id"] = str(doc["job"]["_id"])
            result.append(doc)

        return result

    except Exception as e:
        print("Get Saved Jobs Error:", e)
        return []
