"""
Module: demo_cases.py
Purpose: Demonstrate academic risk and performance evaluation across 3 distinct
         undergraduate student profiles at Sapthagiri NPS University, Bengaluru.
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import sys
import joblib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from predict import predict_student_performance

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_demonstration():
    model = joblib.load('model/best_model.joblib')

    profiles = [
        {
            'title': 'Case 1: Student with High Academic Risk Profile',
            'data': {
                'Section': 'Section C',
                'Gender': 'Male',
                'Previous_Semester_Performance': 'At Risk',
                'Extracurricular_Participation': 'No',
                'Age': 21,
                'Previous_CGPA': 4.85,
                'Attendance_Percentage': 56.0,
                'Absence_Days': 20,
                'Daily_Study_Hours': 1.2,
                'Weekly_Library_Hours': 0.5,
                'Online_Learning_Hours': 1.5,
                'Assignment_Completion_Percentage': 50.0,
                'Internal_Assessment_Marks': 42.0,
                'Backlogs': 3,
                'Marks_Mathematics': 38.0,
                'Marks_DSA': 41.0,
                'Marks_DBMS': 48.0,
                'Marks_OS': 39.0,
                'Marks_CN': 44.0,
                'Marks_DMW': 45.0
            }
        },
        {
            'title': 'Case 2: Average Student with Borderline Attendance',
            'data': {
                'Section': 'Section B',
                'Gender': 'Female',
                'Previous_Semester_Performance': 'Second Class',
                'Extracurricular_Participation': 'Yes',
                'Age': 20,
                'Previous_CGPA': 6.80,
                'Attendance_Percentage': 73.5,
                'Absence_Days': 12,
                'Daily_Study_Hours': 2.5,
                'Weekly_Library_Hours': 2.0,
                'Online_Learning_Hours': 4.0,
                'Assignment_Completion_Percentage': 78.0,
                'Internal_Assessment_Marks': 65.0,
                'Backlogs': 1,
                'Marks_Mathematics': 58.0,
                'Marks_DSA': 62.0,
                'Marks_DBMS': 71.0,
                'Marks_OS': 64.0,
                'Marks_CN': 66.0,
                'Marks_DMW': 69.0
            }
        },
        {
            'title': 'Case 3: High Distinction Performer Profile',
            'data': {
                'Section': 'Section A',
                'Gender': 'Female',
                'Previous_Semester_Performance': 'Distinction',
                'Extracurricular_Participation': 'Yes',
                'Age': 20,
                'Previous_CGPA': 9.20,
                'Attendance_Percentage': 94.0,
                'Absence_Days': 3,
                'Daily_Study_Hours': 4.5,
                'Weekly_Library_Hours': 6.0,
                'Online_Learning_Hours': 6.5,
                'Assignment_Completion_Percentage': 98.0,
                'Internal_Assessment_Marks': 91.0,
                'Backlogs': 0,
                'Marks_Mathematics': 92.0,
                'Marks_DSA': 88.0,
                'Marks_DBMS': 95.0,
                'Marks_OS': 89.0,
                'Marks_CN': 90.0,
                'Marks_DMW': 93.0
            }
        }
    ]

    print("=" * 78)
    print("SAPTHAGIRI NPS UNIVERSITY, BENGALURU")
    print("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (5th SEMESTER)")
    print("ACADEMIC PERFORMANCE PREDICTION & EARLY WARNING DEMONSTRATION")
    print("=" * 78)

    for p in profiles:
        res = predict_student_performance(p['data'], pipeline=model)
        print(f"\n>>> {p['title']}")
        print(f"    * Predicted Final Score   : {res['final_score']} / 100")
        print(f"    * Performance Category    : {res['performance_category']}")
        print(f"    * Early Warning Tier      : {res['academic_risk_level']}")
        print("    * Actionable Guidance     :")
        for rec in res['recommendations']:
            print(f"      - {rec}")

    print("\n" + "=" * 78)

if __name__ == "__main__":
    run_demonstration()
