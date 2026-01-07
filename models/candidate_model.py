# models/candidate_model.py
from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
candidates = db.candidates


def create_candidate(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = candidates.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_candidates():
    cursor = candidates.find().sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])  # ObjectId to string
        result.append(doc)

    return result
