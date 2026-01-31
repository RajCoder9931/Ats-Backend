import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=5000
)

db = client.ERPApp
