import os
# from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_database("papers")
user_collection = db.get_collection("users")
paper_collection = db.get_collection("papers")