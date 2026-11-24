import os
import razorpay
from fastapi import HTTPException

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

def create_payment_order(amount):
    if not os.getenv("RAZORPAY_KEY_ID") or not os.getenv("RAZORPAY_KEY_SECRET"):
        raise HTTPException(status_code=500, detail="Payment configuration missing")

    try:
        order = client.order.create({
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })
        return order
    except Exception:
        raise HTTPException(status_code=502, detail="Unable to create payment order")


def verify_payment(payment_id, order_id, signature):
    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        return True
    except Exception:
        return False
