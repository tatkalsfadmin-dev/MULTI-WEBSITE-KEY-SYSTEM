import sqlite3

DB_NAME = "tatkal_store.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        validity INTEGER NOT NULL,
        website_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS licences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        product_id INTEGER,
        licence_key TEXT,
        expiry_date TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        product_id INTEGER,
        payment_id TEXT UNIQUE,
        utr TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")
  
