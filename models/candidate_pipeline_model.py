from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
candidate_pipelines = db.candidate_pipelines


def create_candidate_pipeline(data):
    now = datetime.datetime.utcnow()

    try:
        pipeline = {
            "candidateId": ObjectId(data.get("candidateId")),
            "jobPostingId": ObjectId(data.get("jobPostingId")),
            "opportunityId": ObjectId(data.get("opportunityId")) if data.get("opportunityId") else None,

            "candidateSnapshot": {
                "name": data.get("candidateName"),
                "email": data.get("candidateEmail"),
                "phone": data.get("candidatePhone"),
                "resumeUrl": data.get("resumeUrl")
            },

            "ats": {
                "score": data.get("atsScore"),
                "result": data.get("atsResult"),
                "parsedSkills": data.get("parsedSkills", []),
                "matchedKeywords": data.get("matchedKeywords", []),
                "screeningStatus": data.get("screeningStatus", "Pending")
            },

            "hrInterview": {
                "status": data.get("hrStatus", "Pending"),
                "feedback": data.get("hrFeedback"),
                "score": data.get("hrScore"),
                "interviewDate": data.get("hrInterviewDate")
            },

            "technicalInterview": {
                "status": data.get("techStatus", "Pending"),
                "feedback": data.get("techFeedback"),
                "score": data.get("techScore"),
                "interviewDate": data.get("techInterviewDate")
            },

            "offer": {
                "status": data.get("offerStatus", "Pending"),
                "offerLetterUrl": data.get("offerLetterUrl"),
                "joiningDate": data.get("joiningDate")
            },

            "currentStage": data.get("currentStage", "Applied"),
            "finalStatus": data.get("finalStatus", "Active"),
            "rejectionReason": data.get("rejectionReason"),
            "remarks": data.get("remarks"),

            "isActive": True,
            "createdBy": data.get("createdBy"),

            "appliedAt": now,
            "completedAt": None,
            "createdAt": now,
            "updatedAt": now
        }

        result = candidate_pipelines.insert_one(pipeline)

        pipeline["_id"] = str(result.inserted_id)
        pipeline["candidateId"] = str(pipeline["candidateId"])
        pipeline["jobPostingId"] = str(pipeline["jobPostingId"])
        if pipeline["opportunityId"]:
            pipeline["opportunityId"] = str(pipeline["opportunityId"])

        return pipeline

    except Exception as e:
        print("Create Candidate Pipeline Error:", e)
        return None


def _serialize_pipeline(doc):
    doc["_id"] = str(doc["_id"])
    doc["candidateId"] = str(doc["candidateId"])
    doc["jobPostingId"] = str(doc["jobPostingId"])
    if doc.get("opportunityId"):
        doc["opportunityId"] = str(doc["opportunityId"])
    return doc


def get_active_pipelines():
    cursor = candidate_pipelines.find(
        {"isActive": True}
    ).sort("createdAt", -1)

    return [_serialize_pipeline(doc) for doc in cursor]


def get_inactive_pipelines():
    cursor = candidate_pipelines.find(
        {"isActive": False}
    ).sort("updatedAt", -1)

    return [_serialize_pipeline(doc) for doc in cursor]


def get_pipeline_by_id(pipeline_id):
    try:
        pipeline = candidate_pipelines.find_one({"_id": ObjectId(pipeline_id)})
        if not pipeline:
            return None
        return _serialize_pipeline(pipeline)
    except Exception:
        return None


def deactivate_pipeline(pipeline_id):
    try:
        result = candidate_pipelines.update_one(
            {"_id": ObjectId(pipeline_id)},
            {"$set": {
                "isActive": False,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False


def activate_pipeline(pipeline_id):
    try:
        result = candidate_pipelines.update_one(
            {"_id": ObjectId(pipeline_id)},
            {"$set": {
                "isActive": True,
                "updatedAt": datetime.datetime.utcnow()
            }}
        )
        return result.modified_count > 0
    except Exception:
        return False
