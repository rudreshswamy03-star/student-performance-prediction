"""
SQLite Database Initializer and Connection Manager
EduPredict AI - Sapthagiri NPS University, Bengaluru
"""

import sqlite3
import hashlib
from typing import Optional, Dict, Any, List
from .config import DB_PATH

def hash_password(password: str) -> str:
    """Standard SHA-256 password hash for demonstration."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database() -> None:
    """Creates required tables and populates default demonstration accounts."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT NOT NULL, -- 'student', 'faculty', 'admin'
        student_id TEXT,    -- e.g. 'SNP001' if student
        department TEXT DEFAULT 'Computer Science and Engineering',
        section TEXT DEFAULT 'Section A',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        type TEXT DEFAULT 'info', -- 'warning', 'info', 'alert', 'success'
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Check and seed default users
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        demo_users = [
            ("student@sapthagiri.edu.in", hash_password("student123"), "Ananya Gowda", "student", "SNP001", "Section A"),
            ("faculty@sapthagiri.edu.in", hash_password("faculty123"), "Prof. K. R. Murthy", "faculty", None, "Section A"),
            ("admin@sapthagiri.edu.in", hash_password("admin123"), "Dean Academic Affairs", "admin", None, None),
        ]
        cursor.executemany("""
        INSERT INTO users (email, password_hash, name, role, student_id, section)
        VALUES (?, ?, ?, ?, ?, ?)
        """, demo_users)

        # Seed initial notifications
        demo_notifications = [
            (1, "Upcoming Internal Assessment", "Continuous Internal Evaluation (CIE-2) for 5th semester begins next Monday.", "info"),
            (1, "Attendance Status Alert", "Your current attendance is 88.5%. Keep it above 75% to maintain exam eligibility.", "success"),
            (2, "Faculty Advisory", "15 students in 5th Sem CSE have been flagged in High Academic Risk category.", "warning"),
            (3, "System Ready", "EduPredict AI model updated with Linear Regression (R²: 0.9277).", "info"),
        ]
        cursor.executemany("""
        INSERT INTO notifications (user_id, title, message, type)
        VALUES (?, ?, ?, ?)
        """, demo_notifications)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("[SUCCESS] SQLite database initialized successfully.")
