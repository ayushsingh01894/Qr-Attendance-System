from flask import (
    Flask, render_template, request,
    redirect, jsonify, send_from_directory
)
from utils.qr_generator import generate_qr
from datetime import datetime
from db import qr_col
import os
import csv

app = Flask(__name__)

ATTENDANCE_FOLDER = "attendance_files"


# ================= HOME =================
@app.route("/")
def home():
    return redirect("/dashboard")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    files = []
    selected_date = request.args.get("date")

    today = datetime.now().strftime("%Y-%m-%d")

    total_sessions = 0
    total_present = 0
    latest_count = 0

    today_sessions = 0
    today_present = 0

    if os.path.exists(ATTENDANCE_FOLDER):
        for f in os.listdir(ATTENDANCE_FOLDER):
            file_path = os.path.join(ATTENDANCE_FOLDER, f)

            if not selected_date or selected_date in f:
                files.append(f)
                total_sessions += 1

                with open(file_path, "r") as file:
                    lines = file.readlines()
                    count = max(len(lines) - 1, 0)
                    total_present += count
                    latest_count = count

            if today in f:
                today_sessions += 1
                with open(file_path, "r") as file:
                    today_present += max(len(file.readlines()) - 1, 0)

    return render_template(
        "dashboard.html",
        files=files,
        total_sessions=total_sessions,
        total_present=total_present,
        latest_count=latest_count,
        today_sessions=today_sessions,
        today_present=today_present
    )


# ================= GENERATE QR =================
@app.route("/generate_qr")
def generate_qr_route():
    qr_id = generate_qr()
    return render_template(
        "generate_qr.html",
        qr_id=qr_id,
        qr_image=f"/static/qr_codes/{qr_id}.png"
    )


# ================= STUDENT FORM =================
@app.route("/attendance/<qr_id>")
def attendance_form(qr_id):
    return render_template("student_form.html", qr_id=qr_id)


# ================= MARK ATTENDANCE =================
@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    data = request.json

    roll_no = data.get("roll_no", "").strip().upper()
    name = data.get("name", "").strip()
    qr_id = data.get("qr_id")

    if not roll_no or not name:
        return jsonify({
            "status": "error",
            "message": "Please fill all details"
        })

    qr_session = qr_col.find_one({
        "qr_id": qr_id,
        "active": True
    })

    if not qr_session:
        return jsonify({
            "status": "error",
            "message": "Invalid QR Code"
        })

    if datetime.now() > qr_session["expires_at"]:
        return jsonify({
            "status": "error",
            "message": "QR Code Expired"
        })

    # ===== FILE LOGIC (1 hour = 1 file) =====
    start_time = qr_session["created_at"]
    date = start_time.strftime("%Y-%m-%d")
    hour = start_time.hour

    filename = f"attendance_{date}_{hour}-{hour+1}.csv"

    os.makedirs(ATTENDANCE_FOLDER, exist_ok=True)
    file_path = os.path.join(ATTENDANCE_FOLDER, filename)

    # ===== DUPLICATE CHECK =====
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            for line in f.readlines():
                if line.startswith(roll_no + ","):
                    return jsonify({
                        "status": "error",
                        "message": "Attendance already marked"
                    })

    # ===== WRITE FILE =====
    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Roll No", "Name", "Time"])

        writer.writerow([
            roll_no,
            name,
            datetime.now().strftime("%H:%M:%S")
        ])

    return jsonify({
        "status": "success",
        "message": "Attendance Submitted Successfully"
    })


# ================= DOWNLOAD ATTENDANCE =================
@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(
        ATTENDANCE_FOLDER,
        filename,
        as_attachment=True
    )


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
