from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
companies = db.companies


def create_company(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = companies.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_companies():
    cursor = companies.find().sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result


def get_company_by_id(company_id):
    try:
        company = companies.find_one({"_id": ObjectId(company_id)})
        if not company:
            return None
        company["_id"] = str(company["_id"])
        return company
    except Exception:
        return None
