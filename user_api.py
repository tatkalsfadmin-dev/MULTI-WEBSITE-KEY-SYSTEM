import sqlite3
from database import DB_NAME


def get_user_history(user_id):
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, product_id, payment_id, status
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (str(user_id),))

    result = [dict(row) for row in cursor.fetchall()]
    db.close()
    return result


def get_user_licences(user_id):
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, product_id, licence_key, expiry_date, status
        FROM licences
        WHERE user_id = ?
        ORDER BY id DESC
    """, (str(user_id),))

    result = [dict(row) for row in cursor.fetchall()]
    db.close()
    return result
