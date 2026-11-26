"""
Authentication Router
EduPredict AI - Sapthagiri NPS University
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from ..database import get_db_connection, hash_password
from ..auth import create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"  # 'student', 'faculty', 'admin'
    student_id: Optional[str] = None
    section: Optional[str] = "Section A"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/login")
def login(req: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed = hash_password(req.password)
    cursor.execute("""
    SELECT id, email, name, role, student_id, department, section 
    FROM users 
    WHERE email = ? AND password_hash = ?
    """, (req.email.lower().strip(), hashed))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid university email or password"
        )

    user_dict = dict(user)
    token = create_access_token({"user_id": user_dict["id"], "role": user_dict["role"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_dict
    }

@router.post("/register")
def register(req: RegisterRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check existing email
    cursor.execute("SELECT id FROM users WHERE email = ?", (req.email.lower().strip(),))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email is already registered")

    hashed = hash_password(req.password)
    cursor.execute("""
    INSERT INTO users (email, password_hash, name, role, student_id, section)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (req.email.lower().strip(), hashed, req.name.strip(), req.role, req.student_id, req.section))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    token = create_access_token({"user_id": user_id, "role": req.role})
    return {
        "message": "Registration successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "name": req.name,
            "email": req.email,
            "role": req.role,
            "student_id": req.student_id,
            "section": req.section
        }
    }

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (req.email.lower().strip(),))
    user = cursor.fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found in university directory")
    return {"message": "Password reset instructions have been dispatched to your university email."}

@router.get("/me")
def get_profile(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/notifications")
def get_notifications(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, title, message, type, is_read, created_at 
    FROM notifications 
    WHERE user_id = ? OR user_id IS NULL
    ORDER BY created_at DESC LIMIT 10
    """, (current_user["id"],))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
