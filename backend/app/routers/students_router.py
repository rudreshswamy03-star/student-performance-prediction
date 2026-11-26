"""
Students API Router
EduPredict AI - Sapthagiri NPS University
"""

import os
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from ..config import DATASET_PATH
from ..auth import get_current_user

router = APIRouter(prefix="/api/students", tags=["Students"])

def get_cohort_dataframe() -> pd.DataFrame:
    if not os.path.exists(DATASET_PATH):
        raise HTTPException(status_code=500, detail="University student dataset not found")
    return pd.read_csv(DATASET_PATH)

@router.get("/me")
def get_my_student_profile(current_user: dict = Depends(get_current_user)):
    """Returns the authenticated student's personalized academic record."""
    student_id = current_user.get("student_id") or "SNP001"
    df = get_cohort_dataframe()
    match = df[df["Student_ID"] == student_id]
    if match.empty:
        # Fallback to first student if not specifically matched
        match = df.head(1)
    return match.iloc[0].to_dict()

@router.get("")
def list_students(
    search: Optional[str] = None,
    section: Optional[str] = None,
    gender: Optional[str] = None,
    risk: Optional[str] = None,
    limit: int = Query(50, ge=1, le=300),
    current_user: dict = Depends(get_current_user)
):
    """Filterable cohort search for students, faculty, and administrators."""
    df = get_cohort_dataframe()

    if search:
        df = df[
            df["Student_ID"].str.contains(search, case=False, na=False) |
            df["Student_Name"].str.contains(search, case=False, na=False)
        ]
    if section and section != "All":
        df = df[df["Section"] == section]
    if gender and gender != "All":
        df = df[df["Gender"] == gender]
    if risk and risk != "All":
        df = df[df["Academic_Risk_Level"] == risk]

    total_matching = len(df)
    results = df.head(limit).to_dict(orient="records")
    return {
        "total": total_matching,
        "returned": len(results),
        "students": results
    }

@router.get("/{student_id}")
def get_student_by_id(student_id: str, current_user: dict = Depends(get_current_user)):
    """Fetches a complete 360-degree student academic card."""
    df = get_cohort_dataframe()
    match = df[df["Student_ID"] == student_id.upper()]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Student ID '{student_id}' not found")
    return match.iloc[0].to_dict()
