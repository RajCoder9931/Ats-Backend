from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
leads = db.leads


def create_lead(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = leads.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_leads(user_id):
    cursor = leads.find({"createdBy": user_id}).sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


 
def get_lead_by_id(lead_id, user_id):
    try:
        lead = leads.find_one({
            "_id": ObjectId(lead_id),
            "createdBy": user_id
        })

        if not lead:
            return None

        lead["_id"] = str(lead["_id"])
        return lead

    except Exception:
        return None
