from pymongo import MongoClient
from config import MONGO_URI
from bson import ObjectId
from datetime import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
notifications = db.notifications


def create_notification(data):
    data["isRead"] = False
    data["createdAt"] = datetime.utcnow().isoformat()
    result = notifications.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_user_notifications(user_id, limit=20):
    cursor = notifications.find(
        {"userId": user_id}
    ).sort("createdAt", -1).limit(limit)

    result = []
    for n in cursor:
        n["_id"] = str(n["_id"])
        result.append(n)

    return result


def mark_notification_read(notification_id):
    notifications.update_one(
        {"_id": ObjectId(notification_id)},
        {"$set": {"isRead": True}}
    )
