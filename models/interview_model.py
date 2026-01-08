from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
interviews = db.interviews

def create_interview(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = interviews.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data

def get_upcoming_interviews():
    return list(
        interviews.find(
            {"status": "Scheduled"},
            {"_id": 0}
        )
    )
