"""
Module: predict.py
Purpose: Standalone inference engine for student academic performance prediction
         at Sapthagiri NPS University, Bengaluru.
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Tuple, List

MODEL_PATH = os.path.join("model", "best_model.joblib")

def load_prediction_model(model_path: str = MODEL_PATH):
    """Loads the serialized trained pipeline (ColumnTransformer + Regressor)."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run train_models.py first.")
    return joblib.load(model_path)

def classify_performance(score: float) -> str:
    """Assigns academic performance category based on demonstration thresholds."""
    if score >= 85.0:
        return "Excellent"
    elif score >= 70.0:
        return "Very Good"
    elif score >= 60.0:
        return "Good"
    elif score >= 50.0:
        return "Average"
    else:
        return "Needs Improvement"

def evaluate_academic_risk(score: float, attendance: float, backlogs: int) -> str:
    """Transparent risk tier rules combining prediction and regulatory academic thresholds."""
    if score < 50.0 or attendance < 65.0 or backlogs >= 3:
        return "High Risk"
    elif score < 60.0 or attendance < 75.0 or backlogs >= 2:
        return "Medium Risk"
    else:
        return "Low Risk"

def generate_personalized_recommendations(student_dict: Dict[str, Any], score: float) -> List[str]:
    """Generates specific, actionable counseling advice based on student weaknesses."""
    recommendations = []

    # Attendance guidance
    att = float(student_dict.get('Attendance_Percentage', 80.0))
    if att < 75.0:
        recommendations.append(f"Attendance is currently at {att:.1f}% (below the university mandatory 75% threshold). Immediate attendance recovery is required to avoid exam debarment.")
    elif att < 85.0:
        recommendations.append("Aim to bring attendance above 85% to maximize continuous internal evaluation (CIE) eligibility.")

    # Study habits
    study_hrs = float(student_dict.get('Daily_Study_Hours', 2.0))
    if study_hrs < 2.5:
        recommendations.append(f"Daily self-study hours ({study_hrs:.1f} hrs) are low for 5th semester engineering. Increase study time to at least 3.5 hours per day.")

    assign_pct = float(student_dict.get('Assignment_Completion_Percentage', 80.0))
    if assign_pct < 70.0:
        recommendations.append(f"Assignment completion is at {assign_pct:.1f}%. Complete remaining lab assignments and mini-projects to secure internal marks.")

    # Backlog guidance
    backlogs = int(student_dict.get('Backlogs', 0))
    if backlogs > 0:
        recommendations.append(f"Student has {backlogs} active backlog(s). Enroll in dedicated department remedial coaching sessions for backlog clearance.")

    # Subject-specific weaknesses
    subjects = {
        'Mathematics': student_dict.get('Marks_Mathematics', 70),
        'Data Structures & Algorithms': student_dict.get('Marks_DSA', 70),
        'Database Management Systems': student_dict.get('Marks_DBMS', 70),
        'Operating Systems': student_dict.get('Marks_OS', 70),
        'Computer Networks': student_dict.get('Marks_CN', 70),
        'Data Mining & Data Wrangling': student_dict.get('Marks_DMW', 70),
    }

    weak_subjects = [subj for subj, mark in subjects.items() if float(mark) < 55.0]
    if weak_subjects:
        subj_str = ", ".join(weak_subjects)
        recommendations.append(f"Targeted remedial study needed in weaker subjects: {subj_str}.")

    if not recommendations:
        recommendations.append("Academic trajectory is strong. Maintain current study routine and consider taking up research projects or competitive programming.")

    return recommendations

def predict_student_performance(student_dict: Dict[str, Any], pipeline=None) -> Dict[str, Any]:
    """
    Given a single student record dictionary, predicts:
    - final_score: Numerical performance score (0 - 100)
    - performance_category: 'Excellent' | 'Very Good' | 'Good' | 'Average' | 'Needs Improvement'
    - risk_level: 'Low Risk' | 'Medium Risk' | 'High Risk'
    - recommendations: List of personalized action points
    """
    if pipeline is None:
        pipeline = load_prediction_model()

    df_single = pd.DataFrame([student_dict])
    pred_raw = float(pipeline.predict(df_single)[0])
    final_score = round(max(0.0, min(100.0, pred_raw)), 2)

    category = classify_performance(final_score)
    risk = evaluate_academic_risk(
        final_score,
        float(student_dict.get('Attendance_Percentage', 80.0)),
        int(student_dict.get('Backlogs', 0))
    )
    recommendations = generate_personalized_recommendations(student_dict, final_score)

    return {
        "final_score": final_score,
        "performance_category": category,
        "academic_risk_level": risk,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    sample_student = {
        'Section': 'Section A',
        'Gender': 'Female',
        'Previous_Semester_Performance': 'First Class',
        'Extracurricular_Participation': 'Yes',
        'Age': 20,
        'Previous_CGPA': 8.45,
        'Attendance_Percentage': 88.5,
        'Absence_Days': 5,
        'Daily_Study_Hours': 3.5,
        'Weekly_Library_Hours': 4.0,
        'Online_Learning_Hours': 5.0,
        'Assignment_Completion_Percentage': 92.0,
        'Internal_Assessment_Marks': 84.0,
        'Backlogs': 0,
        'Marks_Mathematics': 82.0,
        'Marks_DSA': 78.5,
        'Marks_DBMS': 88.0,
        'Marks_OS': 81.0,
        'Marks_CN': 85.0,
        'Marks_DMW': 87.5
    }

    result = predict_student_performance(sample_student)
    print("\n--- SAMPLE PREDICTION: SAPTHAGIRI NPS UNIVERSITY ---")
    print(f"Predicted Final Score      : {result['final_score']} / 100")
    print(f"Performance Category       : {result['performance_category']}")
    print(f"Academic Risk Level        : {result['academic_risk_level']}")
    print("Actionable Recommendations :")
    for r in result['recommendations']:
        print(f"  • {r}")
