# from pymongo import MongoClient
# from config import MONGO_URI

# client = MongoClient(MONGO_URI)
# db = client.authdb
# users = db.users

# def find_by_email(email):
#     return users.find_one({"email": email})

# def create_user(user):
#     return users.insert_one(user)

# def save_refresh_token(user_id, refresh_token):
#     users.update_one({"_id": user_id}, {"$set": {"refresh_token": refresh_token}})

# def find_by_refresh_token(token):
#     return users.find_one({"refresh_token": token})

# def remove_refresh_token(user_id):
#     users.update_one({"_id": user_id}, {"$unset": {"refresh_token": ""}})


###
from bson import ObjectId
from pymongo import MongoClient
from config import MONGO_URI
from utils.password_utils import hash_password, check_password

client = MongoClient(MONGO_URI)
db = client.authdb
users = db.users


def find_by_email(email):
    return users.find_one({"email": email})



def create_user(user):
    return users.insert_one(user)


def find_by_id(user_id):
    try:
        return users.find_one({"_id": ObjectId(user_id)})
    except:
        return None


def update_user(user_id, data):
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": data}
    )
    return find_by_id(user_id)


def change_user_password(user_id, new_password):
    from utils.password_utils import hash_password
    users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hash_password(new_password)}}
    )


def save_refresh_token(user_id, refresh_token):
    users.update_one(
        {"_id": user_id},
        {"$set": {"refresh_token": refresh_token}}
    )


def find_by_refresh_token(token):
    return users.find_one({"refresh_token": token})


def remove_refresh_token(user_id):
    users.update_one(
        {"_id": user_id},
        {"$unset": {"refresh_token": ""}}
    )


