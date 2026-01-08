from datetime import date
from db import db   

candidates = db.candidates
jobs = db.jobs
interviews = db.interviews

def get_dashboard_stats(user_id=None):
    today = date.today().isoformat()

    total_candidates = candidates.count_documents({})
    
    active_jobs = jobs.count_documents({
        "status": {"$in": ["Open", "Active"]}
    })

    interviews_today = interviews.count_documents({
        "date": today
    })


    return {
        "totalCandidates": total_candidates,
        "activeJobs": active_jobs,
        "interviewsToday": interviews_today,
     }
