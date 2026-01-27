import jwt
import datetime
from config import JWT_SECRET, ACCESS_TOKEN_MINUTES 


def generate_access_token(user):
   
    payload = {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],   # admin / super_admin
        "type": "access",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")



def generate_candidate_token(user):
    
    payload = {
        "id": str(user["_id"]),
        "email": user["email"],
        "role": "candidate",
        "type": "candidate",
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=ACCESS_TOKEN_MINUTES),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
