from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
import sqlite3
from database import DB_NAME


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Tatkal Multi Website Key System",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Tatkal Key System"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/products")
def products():
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, name, price, validity, website_id
        FROM products
    """)

    result = [dict(row) for row in cursor.fetchall()]
    db.close()

    return {"products": result}


@app.get("/licences")
def licences():
    db = sqlite3.connect(DB_NAME)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute("""
        SELECT id, user_id, product_id, expiry_date, status
        FROM licences
    """)

    result = [dict(row) for row in cursor.fetchall()]
    db.close()

    return {"licences": result}
from admin import router as admin_router

app.include_router(admin_router)
