
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


# MongoDB setup
MONGO_DB_URL =os.getenv("MONGO_DB_URL")
conn = MongoClient(MONGO_DB_URL)
client = conn

db = client["SCMLITE"]
users = db["User"]
shipment_detail = db["Shipments"]
verification_collection = db["verification_data"]
Device_data=db["device_data"]
feedback_collection = db["feedback_data"]



