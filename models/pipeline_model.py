from db import db
from datetime import datetime
from bson import ObjectId

def assign_job_to_candidate(candidate_id, job_id, job_title):
    db.candidates.update_one(
        {"_id": ObjectId(candidate_id)},
        {
            "$set": {
                "jobId": job_id,
                "jobTitle": job_title,
                "stage": "Assigned",
                "updatedAt": datetime.utcnow().isoformat()
            }
        }
    )
    return db.candidates.find_one({"_id": ObjectId(candidate_id)})

def update_candidate_stage(candidate_id, stage):
    allowed_stages = [
        "Applied",
        "Assigned",
        "Screening",
        "Interview",
        "Machine Round",
        "Hired",
        "Rejected"
    ]

    if stage not in allowed_stages:
        return None

    db.candidates.update_one(
        {"_id": ObjectId(candidate_id)},
        {
            "$set": {
                "stage": stage,
                "updatedAt": datetime.utcnow().isoformat()
            }
        }
    )
    return db.candidates.find_one({"_id": ObjectId(candidate_id)})

def get_candidates_by_job(job_id):
    candidates = list(db.candidates.find({"jobId": job_id}))
    return candidates

def get_candidates_by_stage(stage):
    candidates = list(db.candidates.find({"stage": stage}))
    return candidates

def get_candidate_pipeline(candidate_id):
    return db.candidates.find_one({"_id": ObjectId(candidate_id)})
