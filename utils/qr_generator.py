import qrcode
from datetime import datetime, timedelta
import random
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import qr_col


def generate_qr():
    qr_id = str(random.randint(100000, 999999))  # 6 digit ID

    qr_data = {
        "qr_id": qr_id,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=1),
        "active": True
    }

    qr_col.insert_one(qr_data)

    # 🔥 Professional QR settings
    qr = qrcode.QRCode(
        version=1,              # small & compact
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,              # controls size (try 5–7)
        border=3                 # normal border (real look)
    )

    qr.add_data(
    f"https://qr-attendance-system-5gku.onrender.com/attendance/{qr_id}"
)


    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    qr_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "static",
        "qr_codes",
        f"{qr_id}.png"
    )

    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    img.save(qr_path)

    return qr_id
