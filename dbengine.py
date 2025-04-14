import sqlite3
from app import logging

DB_FILE = "D:\sales_status.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT,
                status INTEGER,
                result TEXT
            )
        """)
        conn.commit()

def insert_sale(uid, status, result):
    logging.info(f"Incert {uid} {status}")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sales (uid, status, result) VALUES (?, ?, ?)", (uid, status, result))
        conn.commit()

def update_sale(uid, status, result):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sales SET status=?, result=? WHERE uid=?", (status, result, uid))
        conn.commit()

def get_sale(uid):
    logging.info(f"Get {uid} ")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE uid=?", (uid,))
        res = cursor.fetchone()
        if res:
            return res[2]  # Индекс 2 — это поле 'status'
        return -10

def get_all_sales():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        return cursor.fetchall()

def delete_sale(uid):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE uid=?", (uid,))
        conn.commit()
