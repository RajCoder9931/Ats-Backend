from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
interview_feedbacks = db.interview_feedbacks


def create_interview_feedback(data):
    now = datetime.datetime.utcnow()

    feedback = {
        "candidateId": ObjectId(data.get("candidateId")),
        "jobPostingId": ObjectId(data.get("jobPostingId")),
        "pipelineId": ObjectId(data.get("pipelineId")),
        "opportunityId": ObjectId(data.get("opportunityId")) if data.get("opportunityId") else None,

        "interviewRound": data.get("interviewRound"),
        "interviewType": data.get("interviewType", "Online"),
        "interviewDate": data.get("interviewDate"),

        "interviewer": {
            "interviewerId": data.get("interviewerId"),
            "name": data.get("interviewerName"),
            "designation": data.get("interviewerDesignation")
        },

        "scores": {
            "communication": data.get("communicationScore"),
            "technical": data.get("technicalScore"),
            "problemSolving": data.get("problemSolvingScore"),
            "attitude": data.get("attitudeScore"),
            "overall": data.get("overallScore")
        },

        "strengths": data.get("strengths"),
        "weaknesses": data.get("weaknesses"),

        "feedback": data.get("feedback"),
        "result": data.get("result"),
        "recommendation": data.get("recommendation"),

        "nextRound": data.get("nextRound"),
        "nextInterviewDate": data.get("nextInterviewDate"),

        "status": data.get("status", "Completed"),

        "isActive": True,
        "createdBy": data.get("createdBy"),

        "createdAt": now,
        "updatedAt": now
    }

    result = interview_feedbacks.insert_one(feedback)

    feedback["_id"] = str(result.inserted_id)
    feedback["candidateId"] = str(feedback["candidateId"])
    feedback["jobPostingId"] = str(feedback["jobPostingId"])
    feedback["pipelineId"] = str(feedback["pipelineId"])
    if feedback["opportunityId"]:
        feedback["opportunityId"] = str(feedback["opportunityId"])

    return feedback


def get_active_feedbacks():
    cursor = interview_feedbacks.find({
        "isActive": True
    }).sort("createdAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["candidateId"] = str(doc["candidateId"])
        doc["jobPostingId"] = str(doc["jobPostingId"])
        doc["pipelineId"] = str(doc["pipelineId"])
        if doc.get("opportunityId"):
            doc["opportunityId"] = str(doc["opportunityId"])
        result.append(doc)

    return result


def get_inactive_feedbacks():
    cursor = interview_feedbacks.find({
        "isActive": False
    }).sort("updatedAt", -1)

    result = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["candidateId"] = str(doc["candidateId"])
        doc["jobPostingId"] = str(doc["jobPostingId"])
        doc["pipelineId"] = str(doc["pipelineId"])
        if doc.get("opportunityId"):
            doc["opportunityId"] = str(doc["opportunityId"])
        result.append(doc)

    return result


def get_feedback_by_id(feedback_id):
    try:
        feedback = interview_feedbacks.find_one({
            "_id": ObjectId(feedback_id)
        })

        if not feedback:
            return None

        feedback["_id"] = str(feedback["_id"])
        feedback["candidateId"] = str(feedback["candidateId"])
        feedback["jobPostingId"] = str(feedback["jobPostingId"])
        feedback["pipelineId"] = str(feedback["pipelineId"])
        if feedback.get("opportunityId"):
            feedback["opportunityId"] = str(feedback["opportunityId"])

        return feedback

    except Exception:
        return None


def deactivate_feedback(feedback_id):
    result = interview_feedbacks.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {
            "isActive": False,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0


def activate_feedback(feedback_id):
    result = interview_feedbacks.update_one(
        {"_id": ObjectId(feedback_id)},
        {"$set": {
            "isActive": True,
            "updatedAt": datetime.datetime.utcnow()
        }}
    )
    return result.modified_count > 0
