import sqlite3
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "inspection_logs.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            weight_kg REAL,
            distance_cm REAL,
            ir_detected BOOLEAN,
            is_pass BOOLEAN,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_inspection(weight_kg: float, distance_cm: float, ir_detected: bool, is_pass: bool, details: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, weight_kg, distance_cm, ir_detected, is_pass, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight_kg, distance_cm, ir_detected, is_pass, details))
    conn.commit()
    conn.close()

def get_recent_logs(limit=10):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append({
            "id": row[0],
            "timestamp": row[1],
            "weight_kg": row[2],
            "distance_cm": row[3],
            "ir_detected": bool(row[4]),
            "is_pass": bool(row[5]),
            "details": row[6]
        })
    return logs

# Initialize DB on import
init_db()
