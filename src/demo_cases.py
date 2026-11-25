"""
Module: demo_cases.py
Purpose: Demonstrate prediction inference on 3 distinct student profiles
         (High-Risk, Borderline, and Distinction).
Course: Data Mining and Data Wrangling
"""

import os
import sys
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import predict_student_grade

# Force UTF-8 on Windows terminal output if possible
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_demonstration():
    model = joblib.load('model/best_model.joblib')

    profiles = [
        {
            'title': 'Case 1: Student A (High Academic Risk Profile)',
            'data': {
                'school': 'GP', 'sex': 'M', 'age': 17, 'address': 'R', 'famsize': 'GT3', 'Pstatus': 'A',
                'Medu': 1, 'Fedu': 1, 'Mjob': 'other', 'Fjob': 'other', 'reason': 'course', 'guardian': 'mother',
                'traveltime': 3, 'studytime': 1, 'failures': 2, 'schoolsup': 'no', 'famsup': 'no',
                'paid': 'no', 'activities': 'no', 'nursery': 'no', 'higher': 'no', 'internet': 'no',
                'romantic': 'yes', 'famrel': 2, 'freetime': 4, 'goout': 5, 'Dalc': 3, 'Walc': 4,
                'health': 2, 'absences': 18, 'G1': 6, 'G2': 6
            }
        },
        {
            'title': 'Case 2: Student B (Average / Borderline Pass Profile)',
            'data': {
                'school': 'GP', 'sex': 'F', 'age': 16, 'address': 'U', 'famsize': 'LE3', 'Pstatus': 'T',
                'Medu': 2, 'Fedu': 2, 'Mjob': 'services', 'Fjob': 'services', 'reason': 'home', 'guardian': 'mother',
                'traveltime': 1, 'studytime': 2, 'failures': 0, 'schoolsup': 'no', 'famsup': 'yes',
                'paid': 'no', 'activities': 'yes', 'nursery': 'yes', 'higher': 'yes', 'internet': 'yes',
                'romantic': 'no', 'famrel': 4, 'freetime': 3, 'goout': 3, 'Dalc': 1, 'Walc': 1,
                'health': 3, 'absences': 4, 'G1': 10, 'G2': 11
            }
        },
        {
            'title': 'Case 3: Student C (Distinction / High Performer Profile)',
            'data': {
                'school': 'GP', 'sex': 'F', 'age': 16, 'address': 'U', 'famsize': 'GT3', 'Pstatus': 'T',
                'Medu': 4, 'Fedu': 4, 'Mjob': 'teacher', 'Fjob': 'health', 'reason': 'reputation', 'guardian': 'mother',
                'traveltime': 1, 'studytime': 4, 'failures': 0, 'schoolsup': 'no', 'famsup': 'yes',
                'paid': 'yes', 'activities': 'yes', 'nursery': 'yes', 'higher': 'yes', 'internet': 'yes',
                'romantic': 'no', 'famrel': 5, 'freetime': 2, 'goout': 1, 'Dalc': 1, 'Walc': 1,
                'health': 5, 'absences': 1, 'G1': 17, 'G2': 18
            }
        }
    ]

    print("=" * 75)
    print("STUDENT PERFORMANCE PREDICTION - MULTI-PROFILE DEMONSTRATION")
    print("=" * 75)

    for p in profiles:
        score, standing, advice = predict_student_grade(p['data'], pipeline=model)
        pct = round((score / 20.0) * 100, 1)
        print(f"\n>>> {p['title']}")
        print(f"    * Predicted Final Exam (G3) : {score} / 20 ({pct}%)")
        print(f"    * Academic Classification   : {standing}")
        print(f"    * Early Warning Advisory    : {advice}")

    print("\n" + "=" * 75)
    print("Execution complete. Streamlit web dashboard active at: http://localhost:8501")
    print("=" * 75)

if __name__ == "__main__":
    run_demonstration()
