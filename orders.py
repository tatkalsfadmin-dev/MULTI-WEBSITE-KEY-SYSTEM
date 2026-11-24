import sqlite3
from database import DB_NAME
from payment import create_payment_order, verify_payment
from licences import generate_licence


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
        INSERT INTO orders (user_id, product_id, status, utr)
        VALUES (?, ?, 'pending', ?)
    """, (str(user_id), product_id, razorpay_order["id"]))

    db.commit()
    db.close()

    return razorpay_order


def confirm_order(order_id, payment_id, signature):
    if not verify_payment(payment_id, order_id, signature):
        return False

    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute("""
        SELECT user_id, product_id
        FROM orders
        WHERE utr = ? AND status = 'pending'
    """, (order_id,))

    order = cursor.fetchone()

    if not order:
        db.close()
        return False

    user_id, product_id = order

    cursor.execute("""
        UPDATE orders
        SET payment_id = ?, status = 'paid'
        WHERE utr = ? AND status = 'pending'
    """, (payment_id, order_id))

    if cursor.rowcount != 1:
        db.close()
        return False

    cursor.execute(
        "SELECT validity FROM products WHERE id = ?",
        (product_id,)
    )
    product = cursor.fetchone()

    db.commit()
    db.close()

    if not product or not product[0]:
        return False

    generate_licence(user_id, product_id, int(product[0]))
    return True
