"""
Module: predict.py
Purpose: Standalone inference script to load the saved best model pipeline
         and predict final marks (G3) for new student academic data.
Course: Data Mining and Data Wrangling
"""

import os
import joblib
import pandas as pd
from typing import Dict, Any, Tuple

MODEL_PATH = os.path.join("model", "best_model.joblib")

def load_prediction_model(model_path: str = MODEL_PATH):
    """Loads the serialized trained pipeline (preprocessor + model)."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Train model first via train_models.py.")
    return joblib.load(model_path)

def predict_student_grade(student_dict: Dict[str, Any], pipeline=None) -> Tuple[float, str, str]:
    """
    Given a single student dictionary containing demographic and academic features,
    returns:
    - predicted_mark: Predicted final exam mark (G3, clipped between 0 and 20)
    - academic_standing: Qualitative grade classification
    - support_recommendation: Actionable academic counseling recommendation
    """
    if pipeline is None:
        pipeline = load_prediction_model()
        
    df_single = pd.DataFrame([student_dict])
    pred_raw = float(pipeline.predict(df_single)[0])
    predicted_mark = round(max(0.0, min(20.0, pred_raw)), 2)
    
    # Classification and Support Assessment
    if predicted_mark >= 16:
        academic_standing = "Distinction / Excellent (>= 16)"
        support_recommendation = "Low Academic Risk: Eligible for advanced enrichment & honor projects."
    elif predicted_mark >= 14:
        academic_standing = "Good Performance (14 - 15)"
        support_recommendation = "Good Standing: On track for strong final exam clearance."
    elif predicted_mark >= 10:
        academic_standing = "Satisfactory / Pass (10 - 13)"
        support_recommendation = "Moderate Standing: Regular practice and study session monitoring advised."
    else:
        academic_standing = "Fail / At Risk (< 10)"
        support_recommendation = "HIGH ACADEMIC RISK: Immediate remedial tutoring and attendance intervention required!"
        
    return predicted_mark, academic_standing, support_recommendation

if __name__ == "__main__":
    # Test sample with a student profile
    sample_student = {
        'school': 'GP', 'sex': 'F', 'age': 16, 'address': 'U', 'famsize': 'GT3', 'Pstatus': 'T',
        'Medu': 4, 'Fedu': 3, 'Mjob': 'services', 'Fjob': 'other', 'reason': 'course', 'guardian': 'mother',
        'traveltime': 1, 'studytime': 3, 'failures': 0, 'schoolsup': 'no', 'famsup': 'yes',
        'paid': 'yes', 'activities': 'yes', 'nursery': 'yes', 'higher': 'yes', 'internet': 'yes',
        'romantic': 'no', 'famrel': 4, 'freetime': 3, 'goout': 2, 'Dalc': 1, 'Walc': 1,
        'health': 5, 'absences': 2, 'G1': 14, 'G2': 15
    }
    
    score, standing, advice = predict_student_grade(sample_student)
    print("\n--- TEST PREDICTION ---")
    print(f"Predicted Final Grade (G3): {score} / 20")
    print(f"Academic Standing: {standing}")
    print(f"Counseling Recommendation: {advice}")
