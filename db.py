import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["qr_code_based_attendence"]

students_col = db["students"]
attendance_col = db["attendance"]
qr_col = db["qr_sessions"]

print("MongoDB Atlas Connected Successfully")