from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

job_applications = db.job_applications
jobs = db.jobs


# ================= CHECK DUPLICATE APPLY =================
def has_already_applied(job_id, candidate_id):
    return job_applications.find_one({
        "jobId": ObjectId(job_id),
        "candidateId": ObjectId(candidate_id)
    })


# ================= APPLY FOR JOB =================
def apply_for_job(job_id, candidate_id):
    application = {
        "jobId": ObjectId(job_id),
        "candidateId": ObjectId(candidate_id),
        "status": "Applied",
        "appliedAt": datetime.datetime.utcnow()
    }

    job_applications.insert_one(application)

    # increment applicants count
    jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$inc": {"applicants": 1}}
    )

    application["_id"] = str(application["_id"])
    application["jobId"] = str(application["jobId"])
    application["candidateId"] = str(application["candidateId"])

    return application


# ================= GET APPLIED JOBS (CANDIDATE) =================
def get_applied_jobs_by_candidate(candidate_id):
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
        {"$sort": {"appliedAt": -1}},
        {
            "$project": {
                "_id": 1,
                "status": 1,
                "appliedAt": 1,
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
    for doc in job_applications.aggregate(pipeline):
        doc["_id"] = str(doc["_id"])
        doc["job"]["_id"] = str(doc["job"]["_id"])
        result.append(doc)

    return result
