import firebase_admin
from firebase_admin import credentials, auth, firestore
from dotenv import load_dotenv
import os

# Initialize
cred = credentials.Certificate("firebase-admin-key.json")
firebase_admin.initialize_app(cred)

load_dotenv()
database_id = os.getenv('DATABASE_ID')

db = firestore.client(database_id=database_id)