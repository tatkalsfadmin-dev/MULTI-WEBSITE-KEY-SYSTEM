import sqlite3
import secrets
from datetime import datetime, timedelta, timezone
from database import DB_NAME


def generate_licence(user_id, product_id, validity_days):
    if validity_days <= 0:
        raise ValueError("Invalid licence validity")

    licence_key = secrets.token_urlsafe(24)
    expiry_date = (
        datetime.now(timezone.utc) + timedelta(days=validity_days)
    ).isoformat()

    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO licences
        (user_id, product_id, licence_key, expiry_date, status)
        VALUES (?, ?, ?, ?, 'active')
    """, (
        str(user_id),
        product_id,
        licence_key,
        expiry_date
    ))

    db.commit()
    db.close()

    return {
        "licence_key": licence_key,
        "expiry_date": expiry_date
    }
