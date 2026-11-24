import os
import hmac
import sqlite3

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
from database import DB_NAME

router = APIRouter(prefix="/admin", tags=["Admin"])


def verify_admin(x_admin_key: str = Header(default="")):
    secret = os.getenv("ADMIN_API_KEY")

    if not secret:
        raise HTTPException(status_code=503, detail="Admin security not configured")

    if not hmac.compare_digest(x_admin_key, secret):
        raise HTTPException(status_code=401, detail="Unauthorized")


class WebsiteInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=8, max_length=500)


class ProductInput(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    validity: int = Field(gt=0)
    website_id: int = Field(gt=0)


@router.post("/websites")
def add_website(data: WebsiteInput, x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO websites (name, url) VALUES (?, ?)",
        (data.name, data.url)
    )

    website_id = cursor.lastrowid
    db.commit()
    db.close()

    return {"success": True, "website_id": website_id}


@router.post("/products")
def add_product(data: ProductInput, x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM websites WHERE id = ?",
        (data.website_id,)
    )

    if not cursor.fetchone():
        db.close()
        raise HTTPException(status_code=404, detail="Website not found")

    cursor.execute("""
        INSERT INTO products (name, price, validity, website_id)
        VALUES (?, ?, ?, ?)
    """, (data.name, data.price, data.validity, data.website_id))

    product_id = cursor.lastrowid
    db.commit()
    db.close()

    return {"success": True, "product_id": product_id}
@router.get("/websites")
def list_websites(x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT * FROM websites")
    result = [dict(row) for row in cursor.fetchall()]

    db.close()
    return {"websites": result}


@router.get("/products")
def list_products(x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("SELECT * FROM products")
    result = [dict(row) for row in cursor.fetchall()]

    db.close()
    return {"products": result}
@router.get("/orders")
def list_orders(x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, user_id, product_id, payment_id, status
        FROM orders
        ORDER BY id DESC
    """)

    result = [dict(row) for row in cursor.fetchall()]
    db.close()

    return {"orders": result}
@router.get("/licences")
def list_licences(x_admin_key: str = Header(default="")):
    verify_admin(x_admin_key)

    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, user_id, product_id, licence_key, expiry_date, status
        FROM licences
        ORDER BY id DESC
    """)

    result = [dict(row) for row in cursor.fetchall()]
    db.close()

    return {"licences": result}
