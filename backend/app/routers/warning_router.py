"""
Early Academic Warning Router
EduPredict AI - Sapthagiri NPS University
"""

import os
import pandas as pd
from fastapi import APIRouter, Depends, Query
from typing import Optional
from ..config import DATASET_PATH
from ..auth import get_current_user

router = APIRouter(prefix="/api/early-warning", tags=["Early Warning System"])

def get_df() -> pd.DataFrame:
    return pd.read_csv(DATASET_PATH)

@router.get("")
def get_early_warning_roster(
    tier: Optional[str] = Query(None, description="'High Risk', 'Medium Risk', or 'Low Risk'"),
    section: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    df = get_df()

    if tier and tier != "All":
        df = df[df["Academic_Risk_Level"] == tier]
    if section and section != "All":
        df = df[df["Section"] == section]

    cols = [
        "Student_ID", "Student_Name", "Section", "Previous_CGPA",
        "Attendance_Percentage", "Backlogs", "Final_Score",
        "Predicted_Performance_Category", "Academic_Risk_Level"
    ]
    records = df[cols].sort_values(by="Final_Score").to_dict(orient="records")

    high_risk_count = int((get_df()["Academic_Risk_Level"] == "High Risk").sum())
    med_risk_count = int((get_df()["Academic_Risk_Level"] == "Medium Risk").sum())
    low_risk_count = int((get_df()["Academic_Risk_Level"] == "Low Risk").sum())

    return {
        "summary": {
            "high_risk_count": high_risk_count,
            "medium_risk_count": med_risk_count,
            "low_risk_count": low_risk_count,
            "total_flagged": len(records)
        },
        "roster": records,
        "protocol": {
            "High Risk": "Mandatory parent-mentor conference, remedial tutoring, weekly attendance check.",
            "Medium Risk": "Faculty counselor guidance, assignment recovery plan, peer study groups.",
            "Low Risk": "Standard academic tracking; research & hackathon encouragement."
        }
    }
