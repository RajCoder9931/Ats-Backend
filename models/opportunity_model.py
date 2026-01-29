# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from config import MONGO_URI
import datetime

client = MongoClient(MONGO_URI)
db = client.ERPApp

opportunities = db.opportunities
contracts = db.contracts


def create_opportunity(data):
    now = datetime.datetime.utcnow()

    opp = {
        "leadId": ObjectId(data.get("leadId")) if data.get("leadId") else None,
        "contractId": ObjectId(data.get("contractId")) if data.get("contractId") else None,

        "companyName": data.get("companyName"),

        "jobTitle": data.get("jobTitle"),
        "jobCode": data.get("jobCode"),
        "jobDescription": data.get("jobDescription"),
        "department": data.get("department"),

        "employmentType": data.get("employmentType", "Full-time"),
        "experienceRequired": data.get("experienceRequired"),
        "skillsRequired": data.get("skillsRequired", []),
        "educationRequired": data.get("educationRequired"),
        "numberOfOpenings": data.get("numberOfOpenings"),

        "jobLocation": {
            "city": data.get("city"),
            "state": data.get("state"),
            "country": data.get("country")
        },

        "workMode": data.get("workMode", "Onsite"),

        "salaryRange": {
            "min": data.get("salaryMin"),
            "max": data.get("salaryMax")
        },

        "opportunityStatus": data.get("opportunityStatus", "Open"),
        "priority": data.get("priority", "Medium"),
        "pipelineStage": data.get("pipelineStage", "Sourcing"),

        "remarks": data.get("remarks"),

        "isActive": True,
        "createdBy": data.get("createdBy"),
        "createdAt": now,
        "updatedAt": now
    }

    result = opportunities.insert_one(opp)

    opp["_id"] = str(result.inserted_id)
    if opp.get("leadId"):
        opp["leadId"] = str(opp["leadId"])
    if opp.get("contractId"):
        opp["contractId"] = str(opp["contractId"])

    return opp


def create_opportunity_from_contract(contract_id, created_by):
    try:
        # Validate ObjectId
        contract_object_id = ObjectId(contract_id)

        contract = contracts.find_one({"_id": contract_object_id})
        if not contract:
            return None, "Contract not found"

        # Prevent duplicate opportunity
        existing = opportunities.find_one({"contractId": contract_object_id})
        if existing:
            return None, "Opportunity already exists for this contract"

        now = datetime.datetime.utcnow()

        opp = {
            "contractId": contract_object_id,
            "leadId": ObjectId(contract.get("leadId")) if contract.get("leadId") else None,

            "companyName": contract.get("companyName"),
            "industry": contract.get("industry"),
            "location": contract.get("location"),
            "contactPerson": contract.get("contactPerson"),

            "jobTitle": "New Job Opening",
            "jobCode": None,
            "jobDescription": "",
            "department": None,

            "employmentType": "Full-time",
            "experienceRequired": None,
            "skillsRequired": [],
            "educationRequired": None,
            "numberOfOpenings": 1,

            "jobLocation": contract.get("location"),
            "workMode": "Onsite",

            "salaryRange": {"min": None, "max": None},

            "opportunityStatus": "Open",
            "priority": "Medium",
            "pipelineStage": "Sourcing",

            "remarks": contract.get("remarks"),

            "isActive": True,
            "createdBy": created_by,
            "createdAt": now,
            "updatedAt": now
        }

        result = opportunities.insert_one(opp)

        
        contracts.update_one(
            {"_id": contract_object_id},
            {"$set": {"opportunityCreated": True, "updatedAt": now}}
        )

        opp["_id"] = str(result.inserted_id)
        opp["contractId"] = str(opp["contractId"])
        if opp.get("leadId"):
            opp["leadId"] = str(opp["leadId"])

        return opp, None

    except InvalidId:
        return None, "Invalid contract id format"

    except Exception as e:
        print("Create opportunity error:", str(e))
        return None, "Server error while creating opportunity"


def get_active_opportunities():
    cursor = opportunities.find({"isActive": True}).sort("createdAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if doc.get("leadId"):
            doc["leadId"] = str(doc["leadId"])
        if doc.get("contractId"):
            doc["contractId"] = str(doc["contractId"])
        result.append(doc)

    return result


def get_inactive_opportunities():
    cursor = opportunities.find({"isActive": False}).sort("updatedAt", -1)
    result = []

    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        if doc.get("leadId"):
            doc["leadId"] = str(doc["leadId"])
        if doc.get("contractId"):
            doc["contractId"] = str(doc["contractId"])
        result.append(doc)

    return result


def get_opportunity_by_id(opp_id):
    try:
        opp = opportunities.find_one({"_id": ObjectId(opp_id)})

        if not opp:
            return None

        opp["_id"] = str(opp["_id"])
        if opp.get("leadId"):
            opp["leadId"] = str(opp["leadId"])
        if opp.get("contractId"):
            opp["contractId"] = str(opp["contractId"])

        return opp

    except Exception:
        return None


def deactivate_opportunity(opp_id):
    result = opportunities.update_one(
        {"_id": ObjectId(opp_id)},
        {"$set": {"isActive": False, "updatedAt": datetime.datetime.utcnow()}}
    )
    return result.modified_count > 0


def activate_opportunity(opp_id):
    result = opportunities.update_one(
        {"_id": ObjectId(opp_id)},
        {"$set": {"isActive": True, "updatedAt": datetime.datetime.utcnow()}}
    )
    return result.modified_count > 0
