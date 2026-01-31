from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI


client = MongoClient(MONGO_URI)
db = client.ERPApp

job_applications = db.job_applications
candidate_profiles = db.candidate_profiles


def calculate_profile_score(candidate):
    """
    Simple weighted profile completion logic
    """
    fields = [
        "name",
        "phone",
        "skills",
        "experience",
        "education",
        "resume_url"
    ]

    filled = 0
    for field in fields:
        if candidate.get(field):
            filled += 1

    total = len(fields)
    percentage = int((filled / total) * 100)

    return {
        "completed_fields": filled,
        "total_fields": total,
        "percentage": percentage
    }


def get_candidate_dashboard_stats(candidate_id):
    try:
        cid = ObjectId(candidate_id)
    except Exception:
        return {"error": "Invalid candidate id"}


    total_applied = job_applications.count_documents({
        "candidateId": cid
    })

    rejected = job_applications.count_documents({
        "candidateId": cid,
        "status": "Rejected"
    })

    interview = job_applications.count_documents({
        "candidateId": cid,
        "status": "Interview"
    })

    selected = job_applications.count_documents({
        "candidateId": cid,
        "status": "Selected"
    })

    
    candidate = candidate_profiles.find_one({"_id": cid})
    profile_score = calculate_profile_score(candidate) if candidate else {}

    return {
        "jobs": {
            "applied": total_applied,
            "rejected": rejected,
            "interview": interview,
            "selected": selected
        },
        "profile": profile_score
    }
