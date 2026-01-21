from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

saved_jobs = db.saved_jobs
jobs = db.jobs

# ================= CHECK ALREADY SAVED =================
def is_job_saved(candidate_id, job_id):
    return saved_jobs.find_one({
        "candidateId": ObjectId(candidate_id),
        "jobId": ObjectId(job_id)
    })


# ================= SAVE JOB =================
def save_job(candidate_id, job_id):
    data = {
        "candidateId": ObjectId(candidate_id),
        "jobId": ObjectId(job_id),
        "savedAt": datetime.datetime.utcnow()
    }
    saved_jobs.insert_one(data)
    return data


# ================= REMOVE SAVED JOB =================
def remove_saved_job(candidate_id, job_id):
    saved_jobs.delete_one({
        "candidateId": ObjectId(candidate_id),
        "jobId": ObjectId(job_id)
    })


# ================= GET SAVED JOBS =================
def get_saved_jobs(candidate_id):
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
