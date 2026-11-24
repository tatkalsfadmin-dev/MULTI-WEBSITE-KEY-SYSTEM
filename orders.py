import sqlite3
from database import DB_NAME
from payment import create_payment_order, verify_payment


def create_order(user_id, product_id):
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products WHERE id = ?",
        (product_id,)
    )
    product = cursor.fetchone()

    if not product:
        db.close()
        raise ValueError("Product not found")

    razorpay_order = create_payment_order(float(product["price"]))

    cursor.execute("""
        INSERT INTO orders (user_id, product_id, status)
        VALUES (?, ?, 'pending')
    """, (str(user_id), product_id))

    cursor.execute("""
        UPDATE orders
        SET utr = ?
        WHERE id = ?
    """, (razorpay_order["id"], cursor.lastrowid))

    db.commit()
    db.close()

    return razorpay_order


def confirm_order(order_id, payment_id, signature):
    if not verify_payment(payment_id, order_id, signature):
        return False

    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute("""
        UPDATE orders
        SET payment_id = ?, status = 'paid'
        WHERE utr = ? AND status = 'pending'
    """, (payment_id, order_id))

    success = cursor.rowcount == 1
    db.commit()
    db.close()

    return success
