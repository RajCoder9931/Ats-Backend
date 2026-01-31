from bson import ObjectId
from pymongo import MongoClient
from config import MONGO_URI
from utils.password_utils import hash_password

client = MongoClient(MONGO_URI)
db = client.authdb
users = db.users


def _serialize_user(user):
    if not user:
        return None
    user["_id"] = str(user["_id"])
    return user


def find_by_email(email):
    try:
        user = users.find_one({"email": email})
        return _serialize_user(user)
    except Exception:
        return None


def create_user(user):
    try:
        result = users.insert_one(user)
        user["_id"] = str(result.inserted_id)
        return user
    except Exception as e:
        print("Create User Error:", e)
        return None


def find_by_id(user_id):
    try:
        user = users.find_one({"_id": ObjectId(user_id)})
        return _serialize_user(user)
    except Exception:
        return None


def update_user(user_id, data):
    try:
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": data}
        )
        return find_by_id(user_id)
    except Exception as e:
        print("Update User Error:", e)
        return None


def change_user_password(user_id, new_password):
    try:
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"password": hash_password(new_password)}}
        )
        return True
    except Exception as e:
        print("Change Password Error:", e)
        return False


def save_refresh_token(user_id, refresh_token):
    try:
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"refresh_token": refresh_token}}
        )
        return True
    except Exception:
        return False


def find_by_refresh_token(token):
    try:
        user = users.find_one({"refresh_token": token})
        return _serialize_user(user)
    except Exception:
        return None


def remove_refresh_token(user_id):
    try:
        users.update_one(
            {"_id": ObjectId(user_id)},
            {"$unset": {"refresh_token": ""}}
        )
        return True
    except Exception:
        return False
