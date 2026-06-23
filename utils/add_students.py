import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import students_col

students = [
    {
        "_id": "MCA101",
        "name": "Ayush Singh",
        "course": "MCA",
        "year": 2
    },
    {
        "_id": "MCA102",
        "name": "Rahul Kumar",
        "course": "MCA",
        "year": 2
    },
    {
        "_id": "MCA103",
        "name": "Neha Sharma",
        "course": "MCA",
        "year": 2
    }
]

for student in students:
    if not students_col.find_one({"_id": student["_id"]}):
        students_col.insert_one(student)

print("Students inserted successfully")
