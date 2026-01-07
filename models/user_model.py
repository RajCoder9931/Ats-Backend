from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.authdb
users = db.users

def find_by_email(email):
    return users.find_one({"email": email})

def create_user(user):
    return users.insert_one(user)

def save_refresh_token(user_id, refresh_token):
    users.update_one({"_id": user_id}, {"$set": {"refresh_token": refresh_token}})

def find_by_refresh_token(token):
    return users.find_one({"refresh_token": token})

def remove_refresh_token(user_id):
    users.update_one({"_id": user_id}, {"$unset": {"refresh_token": ""}})
