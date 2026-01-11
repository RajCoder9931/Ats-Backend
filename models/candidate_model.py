# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from config import MONGO_URI
# import datetime

# client = MongoClient(MONGO_URI)
# db = client.ERPApp
# candidates = db.candidates


# def create_candidate(data):
#     data["createdAt"] = datetime.datetime.utcnow().isoformat()
#     result = candidates.insert_one(data)
#     data["_id"] = str(result.inserted_id)
#     return data


# def get_all_candidates():
#     cursor = candidates.find().sort("createdAt", -1)
#     result = []

#     for doc in cursor:
#         doc["_id"] = str(doc["_id"])
#         result.append(doc)

#     return result


# def get_candidate_by_id(candidate_id):
#     try:
#         return candidates.find_one({"_id": ObjectId(candidate_id)})
#     except:
#         return None

# def update_candidate_by_id(candidate_id, data):
    
#     try:
#         update_fields = {}

#         allowed_fields = [
#             "name",
#             "email",
#             "phone",
#             "location",
#             "country",
#             "state",
#             "locality",
#             "dateOfBirth",
#             "gender",
#             "skills",
#             "currentCompany",
#             "currentPosition",
#             "experience",
#             "notes",
#             "status",
#             "stage"
#         ]

#         for field in allowed_fields:
#             if field in data:
#                 update_fields[field] = data[field]

#         if not update_fields:
#             return None

#         candidates.update_one(
#             {"_id": ObjectId(candidate_id)},
#             {"$set": update_fields}
#         )

#         return candidates.find_one({"_id": ObjectId(candidate_id)})

#     except:
#         return None


##

from pymongo import MongoClient
from bson.objectid import ObjectId
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
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_candidate_by_id(candidate_id):
    try:
        return candidates.find_one({"_id": ObjectId(candidate_id)})
    except:
        return None


def update_candidate_by_id(candidate_id, data):
    try:
        update_fields = {}

        allowed_fields = [
            "name",
            "email",
            "phone",
            "location",
            "country",
            "state",
            "locality",
            "dateOfBirth",
            "gender",
            "skills", 
            "experience",    
            "education",      
            "currentCompany",
            "currentPosition",
            "notes", 
            "status",       # Active / Inactive
            "stage"
        ]

        for field in allowed_fields:
            if field in data:
                update_fields[field] = data[field]

        if not update_fields:
            return None

        update_fields["updatedAt"] = datetime.datetime.utcnow().isoformat()

        candidates.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_fields}
        )

        return candidates.find_one({"_id": ObjectId(candidate_id)})

    except Exception as e:
        print("Update Candidate Error:", e)
        return None
