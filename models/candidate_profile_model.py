from bson import ObjectId
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.authdb
users = db.users   # same users collection


def create_candidate_profile(data):
    data["role"] = "candidate"
    return users.insert_one(data)


def find_candidate_by_email_and_role(email):
    return users.find_one({
        "email": email,
        "role": "candidate"
    })


def find_candidate_profile_by_id(candidate_id):
    try:
        return users.find_one({
            "_id": ObjectId(candidate_id),
            "role": "candidate"
        })
    except:
        return None


def update_candidate_profile(candidate_id, data):
    users.update_one(
        {
            "_id": ObjectId(candidate_id),
            "role": "candidate"
        },
        {"$set": data}
    )
    return find_candidate_profile_by_id(candidate_id)
