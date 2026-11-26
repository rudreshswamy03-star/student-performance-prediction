"""
Academics API Router
EduPredict AI - Sapthagiri NPS University
"""

import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from ..config import DATASET_PATH
from ..auth import get_current_user

router = APIRouter(prefix="/api/academics", tags=["Academics"])

def get_df() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)

@router.get("/subjects")
def get_subject_statistics(current_user: dict = Depends(get_current_user)):
    """Returns batch statistics for all six 5th semester core subjects."""
    df = get_df()
    subject_map = [
        {"code": "CS501", "name": "Mathematics", "column": "Marks_Mathematics", "credits": 4},
        {"code": "CS502", "name": "Data Structures & Algorithms", "column": "Marks_DSA", "credits": 4},
        {"code": "CS503", "name": "Database Management Systems", "column": "Marks_DBMS", "credits": 4},
        {"code": "CS504", "name": "Operating Systems", "column": "Marks_OS", "credits": 3},
        {"code": "CS505", "name": "Computer Networks", "column": "Marks_CN", "credits": 3},
        {"code": "CS506", "name": "Data Mining and Data Wrangling", "column": "Marks_DMW", "credits": 4},
    ]

    results = []
    for s in subject_map:
        col = s["column"]
        results.append({
            "code": s["code"],
            "subject_name": s["name"],
            "credits": s["credits"],
            "average_marks": round(float(df[col].mean()), 1),
            "median_marks": round(float(df[col].median()), 1),
            "highest_marks": round(float(df[col].max()), 1),
            "lowest_marks": round(float(df[col].min()), 1),
            "pass_rate_percentage": round(float((df[col] >= 40).mean() * 100), 1)
        })
    return results

@router.get("/analytics")
def get_cohort_analytics(current_user: dict = Depends(get_current_user)):
    """Returns high-level university cohort metrics."""
    df = get_df()
    return {
        "cohort_size": len(df),
        "department": "Computer Science and Engineering",
        "semester": "5th Semester",
        "average_cgpa": round(float(df["Previous_CGPA"].mean()), 2),
        "average_attendance": round(float(df["Attendance_Percentage"].mean()), 1),
        "average_study_hours": round(float(df["Daily_Study_Hours"].mean()), 1),
        "average_final_score": round(float(df["Final_Score"].mean()), 1),
        "risk_breakdown": df["Academic_Risk_Level"].value_counts().to_dict(),
        "performance_breakdown": df["Predicted_Performance_Category"].value_counts().to_dict(),
        "section_breakdown": df["Section"].value_counts().to_dict()
    }

@router.get("/report/{student_id}")
def generate_student_report(student_id: str, current_user: dict = Depends(get_current_user)):
    """Generates an academic evaluation report for an individual student."""
    df = get_df()
    match = df[df["Student_ID"] == student_id.upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail="Student not found")

    student = match.iloc[0].to_dict()
    return {
        "institution": "Sapthagiri NPS University, Bengaluru",
        "student_id": student["Student_ID"],
        "student_name": student["Student_Name"],
        "department": student["Department"],
        "section": student["Section"],
        "cgpa": student["Previous_CGPA"],
        "attendance": student["Attendance_Percentage"],
        "backlogs": student["Backlogs"],
        "final_predicted_score": student["Final_Score"],
        "performance_tier": student["Predicted_Performance_Category"],
        "risk_level": student["Academic_Risk_Level"],
        "subject_marks": {
            "Mathematics": student["Marks_Mathematics"],
            "Data Structures & Algorithms": student["Marks_DSA"],
            "Database Management Systems": student["Marks_DBMS"],
            "Operating Systems": student["Marks_OS"],
            "Computer Networks": student["Marks_CN"],
            "Data Mining & Data Wrangling": student["Marks_DMW"]
        }
    }
