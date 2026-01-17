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
