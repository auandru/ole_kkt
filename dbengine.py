import sqlite3
import logging
import log_config

logger = logging.getLogger(__name__)

DB_FILE = "D:\sales_status.db"

def init_db():
    logger.info(f" Init DB ")
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
    logger.info(f"Incert {uid} {status}")
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
    logger.info(f"Get {uid} ")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales WHERE uid=?", (uid,))
        res = cursor.fetchone()
        if res:
            logger.info(res[2])
            return res[2]  # Индекс 2 — это поле 'status'
        logger.info(-10)
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
