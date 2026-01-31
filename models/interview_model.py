from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
interviews = db.interviews


def create_interview(data):
    try:
        data["createdAt"] = datetime.datetime.utcnow().isoformat()
        result = interviews.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return data
    except Exception as e:
        print("Create Interview Error:", e)
        return None


def get_upcoming_interviews():
    try:
        cursor = interviews.find(
            {"status": "Scheduled"}
        )

        result = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            result.append(doc)

        return result

    except Exception as e:
        print("Get Upcoming Interviews Error:", e)
        return []
