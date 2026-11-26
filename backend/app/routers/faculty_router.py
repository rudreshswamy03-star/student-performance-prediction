"""
Faculty & Administrator API Routers
EduPredict AI - Sapthagiri NPS University
"""

import os
import json
import pandas as pd
from fastapi import APIRouter, Depends
from ..config import DATASET_PATH, METRICS_PATH
from ..auth import get_current_user, require_role

faculty_router = APIRouter(prefix="/api/faculty", tags=["Faculty Operations"])
admin_router = APIRouter(prefix="/api/admin", tags=["Administrator Operations"])

def get_df() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)

# ----------------- FACULTY ENDPOINTS -----------------
@faculty_router.get("/dashboard")
def get_faculty_dashboard(current_user: dict = Depends(require_role(["faculty", "admin"]))):
    df = get_df()
    sec = current_user.get("section") or "Section A"
    sec_df = df[df["Section"] == sec]

    return {
        "faculty_name": current_user["name"],
        "assigned_section": sec,
        "section_student_count": len(sec_df),
        "section_avg_cgpa": round(float(sec_df["Previous_CGPA"].mean()), 2),
        "section_avg_attendance": round(float(sec_df["Attendance_Percentage"].mean()), 1),
        "section_avg_score": round(float(sec_df["Final_Score"].mean()), 1),
        "high_risk_count": int((sec_df["Academic_Risk_Level"] == "High Risk").sum()),
        "medium_risk_count": int((sec_df["Academic_Risk_Level"] == "Medium Risk").sum()),
        "recent_alerts": [
            f"Attendance reminder: {int((sec_df['Attendance_Percentage'] < 75).sum())} students in {sec} below 75%",
            f"CIE Assessment completed for 5th semester",
            f"Remedial coaching schedules published"
        ]
    }

# ----------------- ADMIN ENDPOINTS -----------------
@admin_router.get("/metrics")
def get_admin_metrics(current_user: dict = Depends(require_role(["admin"]))):
    df = get_df()
    model_metrics = {}
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            model_metrics = json.load(f)

    return {
        "institution": "Sapthagiri NPS University, Bengaluru",
        "cohort_size": len(df),
        "total_active_sections": 3,
        "overall_pass_rate": round(float((df["Final_Score"] >= 50).mean() * 100), 1),
        "high_risk_percentage": round(float((df["Academic_Risk_Level"] == "High Risk").mean() * 100), 1),
        "active_machine_learning_model": model_metrics.get("best_model_name", "Linear Regression"),
        "benchmark_results": model_metrics.get("metrics", {}),
        "feature_importances": model_metrics.get("feature_importances", [])
    }
