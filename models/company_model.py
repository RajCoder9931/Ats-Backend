# models/company_model.py
from pymongo import MongoClient
from bson import ObjectId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ATS
companies = db.companies


def create_company(data):
    data["createdDate"] = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    data["stats"] = {
        "candidates": 0,
        "totalCandidates": 0,
        "contacts": 0,
        "totalContacts": 0,
        "paidUsers": 0,
        "totalUsers": 1,
        "storageUsed": "0 MB",
    }

    result = companies.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_companies():
    result = []
    for c in companies.find():
        c["_id"] = str(c["_id"])
        result.append(c)
    return result


def get_company_by_id(company_id):
    company = companies.find_one({"_id": ObjectId(company_id)})
    if not company:
        return None
    company["_id"] = str(company["_id"])
    return company
