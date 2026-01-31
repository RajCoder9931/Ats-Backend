from db import db
from datetime import datetime
from bson import ObjectId


def _serialize_candidate(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


def assign_job_to_candidate(candidate_id, job_id, job_title):
    try:
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
        candidate = db.candidates.find_one({"_id": ObjectId(candidate_id)})
        return _serialize_candidate(candidate)

    except Exception as e:
        print("Assign Job Error:", e)
        return None


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

    try:
        db.candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {
                "$set": {
                    "stage": stage,
                    "updatedAt": datetime.utcnow().isoformat()
                }
            }
        )
        candidate = db.candidates.find_one({"_id": ObjectId(candidate_id)})
        return _serialize_candidate(candidate)

    except Exception as e:
        print("Update Candidate Stage Error:", e)
        return None


def get_candidates_by_job(job_id):
    try:
        candidates = list(db.candidates.find({"jobId": job_id}))
        return [_serialize_candidate(c) for c in candidates]
    except Exception as e:
        print("Get Candidates By Job Error:", e)
        return []


def get_candidates_by_stage(stage):
    try:
        candidates = list(db.candidates.find({"stage": stage}))
        return [_serialize_candidate(c) for c in candidates]
    except Exception as e:
        print("Get Candidates By Stage Error:", e)
        return []


def get_candidate_pipeline(candidate_id):
    try:
        candidate = db.candidates.find_one({"_id": ObjectId(candidate_id)})
        return _serialize_candidate(candidate)
    except Exception:
        return None
