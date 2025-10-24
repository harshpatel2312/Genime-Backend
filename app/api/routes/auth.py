from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_admin import auth
from app.core.firebase_config import db
import logging
import os


router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


# Schemas
class SignUpRequest(BaseModel):
    email: str
    password: str
    username: str

class LoginRequest(BaseModel):
    email: str
    password: str

# SignUp
@router.post("/signup")
async def signup_user(req: SignUpRequest):
    try:
        logger.info(f"Routes------/auth/signup------active")
        user = auth.create_user(
            email=req.email,
            password=req.password,
            display_name=req.username,
        )

        # Store in firestore
        db.collection("users").document(user.uid).set({
            "email": req.email,
            "username": req.username,
            "uid": user.uid
        }, merge=True)

        logger.info(f"Firestore------Data Stored")

        return {"status": "success", "message": "User created successfully", "uid": user.uid}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login
@router.post("/login")
async def login_user(req: LoginRequest):
    try:
        logger.info(f"Routes------/auth/login------active")
        import requests
        from dotenv import load_dotenv
        import os

        load_dotenv()
        api_key = os.getenv("FIRESTORE_API_KEY")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        logger.info(f"FIRESTORE_API_KEY------Fetched")

        payload = {
            "email": req.email,
            "password": req.password,
            "returnSecureToken": True
        }

        logger.info(f"Login------Sending Payload")

        res = requests.post(url, json=payload)
        data = res.json()

        if "idToken" not in data:
            raise HTTPException(status_code=401, detail=data.get("error", {}).get("message", "Invalid credentials"))

        # Retrieve username from firestore
        user_docs = db.collection("users").where("email", "==", req.email).get()
        username = None
        if user_docs:
              username = user_docs[0].to_dict().get("username")

        return {"status": "success", "idToken": data["idToken"], "user": {"username": username or req.email}}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))