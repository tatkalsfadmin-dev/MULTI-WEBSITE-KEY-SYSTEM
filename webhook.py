import os
import hmac
import hashlib
import json

from fastapi import APIRouter, Request, Header, HTTPException

router = APIRouter()


@router.post("/razorpay/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(default="")
):
    secret = os.getenv("RAZORPAY_WEBHOOK_SECRET")

    if not secret:
        raise HTTPException(
            status_code=503,
            detail="Webhook secret is not configured"
        )

    body = await request.body()

    expected_signature = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(
        expected_signature,
        x_razorpay_signature
    ):
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = json.loads(body)

    return {
        "received": True,
        "event": event.get("event")
    }
