# -*- coding: utf-8 -*-

from pymongo import MongoClient
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp
jobs = db.jobs


def create_job(data):
    data["createdAt"] = datetime.datetime.utcnow().isoformat()
    result = jobs.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data


def get_all_jobs():
    cursor = jobs.find().sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        result.append(doc)

    return result
