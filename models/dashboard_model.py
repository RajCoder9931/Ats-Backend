from datetime import date
from db import db

candidates = db.candidates
jobs = db.jobs
interviews = db.interviews


def get_dashboard_stats(user_id=None):
    today = date.today().isoformat()

    total_candidates = candidates.count_documents({
        "createdBy": user_id
    })

    active_jobs = jobs.count_documents({
        "status": {"$in": ["Open", "Active"]},
        "createdBy": user_id
    })

    interviews_today = interviews.count_documents({
        "date": today,
        "createdBy": user_id
    })

     
    pipeline = [
        {"$match": {"createdBy": user_id}},
        {
            "$group": {
                "_id": "$stage",
                "count": {"$sum": 1}
            }
        }
    ]

    stage_data = candidates.aggregate(pipeline)

    stage_counts = {
        "Applied": 0,
        "Screening": 0,
        "Interview": 0,
        "Hired": 0
    }

    for item in stage_data:
        stage = item["_id"]
        if stage in stage_counts:
            stage_counts[stage] = item["count"]

    return {
        "totalCandidates": total_candidates,
        "activeJobs": active_jobs,
        "interviewsToday": interviews_today,
        "candidateStages": stage_counts
    }
