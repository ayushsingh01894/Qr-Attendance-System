from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ayushsingh01894_db_user:ayush1234@ayush.kzpuq17.mongodb.net/?retryWrites=true&w=majority&appName=Ayush"

client = MongoClient(MONGO_URI)

db = client["qr_code_based_attendence"]

students_col = db["students"]
attendance_col = db["attendance"]
qr_col = db["qr_sessions"]

print("MongoDB Atlas Connected Successfully")