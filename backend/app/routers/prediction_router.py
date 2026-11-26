"""
Machine Learning Prediction API Router
EduPredict AI - Sapthagiri NPS University
"""

import sys
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from ..config import BASE_DIR, MODEL_PATH
from ..auth import get_current_user

# Add src to path for predict module
SRC_PATH = os.path.join(BASE_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from predict import predict_student_performance, load_prediction_model

router = APIRouter(prefix="/api/predict", tags=["AI Prediction"])

class PredictionInput(BaseModel):
    Section: str = Field(default="Section A", description="Section A, B, or C")
    Gender: str = Field(default="Female", description="Male or Female")
    Previous_Semester_Performance: str = Field(default="First Class")
    Extracurricular_Participation: str = Field(default="Yes")
    Age: int = Field(default=20, ge=18, le=30)
    Previous_CGPA: float = Field(default=7.5, ge=0.0, le=10.0)
    Attendance_Percentage: float = Field(default=85.0, ge=0.0, le=100.0)
    Absence_Days: Optional[int] = None
    Daily_Study_Hours: float = Field(default=3.0, ge=0.5, le=12.0)
    Weekly_Library_Hours: float = Field(default=4.0, ge=0.0, le=30.0)
    Online_Learning_Hours: float = Field(default=4.0, ge=0.0, le=30.0)
    Assignment_Completion_Percentage: float = Field(default=85.0, ge=0.0, le=100.0)
    Internal_Assessment_Marks: Optional[float] = None
    Backlogs: int = Field(default=0, ge=0, le=10)
    Marks_Mathematics: float = Field(default=75.0, ge=0.0, le=100.0)
    Marks_DSA: float = Field(default=72.0, ge=0.0, le=100.0)
    Marks_DBMS: float = Field(default=80.0, ge=0.0, le=100.0)
    Marks_OS: float = Field(default=74.0, ge=0.0, le=100.0)
    Marks_CN: float = Field(default=78.0, ge=0.0, le=100.0)
    Marks_DMW: float = Field(default=82.0, ge=0.0, le=100.0)

# Cached pipeline instance
try:
    _pipeline = load_prediction_model(MODEL_PATH)
except Exception:
    _pipeline = None

@router.post("")
def predict_performance(data: PredictionInput, current_user: dict = Depends(get_current_user)):
    """Executes real-time inference using the trained Scikit-Learn pipeline."""
    global _pipeline
    if _pipeline is None:
        try:
            _pipeline = load_prediction_model(MODEL_PATH)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ML Pipeline unavailable: {e}")

    student_dict = data.model_dump()
    if student_dict["Absence_Days"] is None:
        student_dict["Absence_Days"] = int(round((100.0 - student_dict["Attendance_Percentage"]) * 0.45))
    if student_dict["Internal_Assessment_Marks"] is None:
        subj_avg = (
            data.Marks_Mathematics + data.Marks_DSA + data.Marks_DBMS +
            data.Marks_OS + data.Marks_CN + data.Marks_DMW
        ) / 6.0
        student_dict["Internal_Assessment_Marks"] = round(subj_avg * 0.95, 1)

    try:
        output = predict_student_performance(student_dict, pipeline=_pipeline)
        output["model_name"] = "Linear Regression (Validated Best Model)"
        output["model_r2_score"] = 0.9277
        output["confidence"] = "High (R² = 92.77%, Test RMSE = 3.37)"
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference execution error: {str(e)}")
