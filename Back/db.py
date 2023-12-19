from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
from fastapi import Depends
from pymongo import MongoClient

# MongoDB setup
MONGO_DB_URL = "mongodb+srv://sanjaiR:SanjaiR@sanjai1.e51bhcy.mongodb.net/?retryWrites=true&w=majority"
conn = MongoClient(MONGO_DB_URL)
client = conn
db = client["SCMLITE"]
users = db["User"]
shipment_detail = db["Shipments"]
verification_collection = db["verification_data"]
Device_data=db["device_data"]


