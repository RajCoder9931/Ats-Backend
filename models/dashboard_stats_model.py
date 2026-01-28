from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.ERPApp

leads = db.leads
contact_logs = db.contact_logs
opportunities = db.opportunities
job_postings = db.job_postings
interview_feedbacks = db.interview_feedbacks


def get_dashboard_stats():
    stats = {
        "totalLeads": leads.count_documents({"isActive": True}),
        "totalContacts": contact_logs.count_documents({"isActive": True}),
        "totalOpportunities": opportunities.count_documents({"isActive": True}),
        "totalJobPostings": job_postings.count_documents({"isActive": True}),
        "totalInterviews": interview_feedbacks.count_documents({"isActive": True})
    }

    return stats
