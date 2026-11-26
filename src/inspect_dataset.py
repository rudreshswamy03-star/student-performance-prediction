"""
Module: inspect_dataset.py
Purpose: Inspect the Sapthagiri NPS University student cohort dataset.
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import pandas as pd

def inspect_university_dataset(filepath: str = "dataset/university_students.csv") -> None:
    if not os.path.exists(filepath):
        from generate_university_data import save_university_dataset
        filepath = save_university_dataset(filepath)

    df = pd.read_csv(filepath)

    print("=" * 78)
    print("SAPTHAGIRI NPS UNIVERSITY, BENGALURU")
    print("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    print("5TH SEMESTER COHORT DATASET INSPECTION")
    print("=" * 78)
    print(f"Total Student Records : {df.shape[0]}")
    print(f"Total Attributes      : {df.shape[1]}")
    print(f"Missing Values        : {df.isnull().sum().sum()}")
    print(f"Duplicate Student IDs : {df.duplicated(subset=['Student_ID']).sum()}")

    print("\n--- FIRST 5 RECORDS ---")
    print(df[['Student_ID', 'Student_Name', 'Section', 'Previous_CGPA', 'Attendance_Percentage', 'Backlogs', 'Final_Score', 'Predicted_Performance_Category']].head())

    print("\n--- ATTRIBUTE DATA TYPES & NON-NULL SUMMARY ---")
    df.info()

    print("\n--- SUMMARY STATISTICS OF ACADEMIC SUBJECTS ---")
    subjects = ['Marks_Mathematics', 'Marks_DSA', 'Marks_DBMS', 'Marks_OS', 'Marks_CN', 'Marks_DMW']
    print(df[subjects].describe())

    print("\n--- PERFORMANCE CATEGORY DISTRIBUTION ---")
    print(df['Predicted_Performance_Category'].value_counts())

    print("\n--- ACADEMIC RISK LEVEL DISTRIBUTION ---")
    print(df['Academic_Risk_Level'].value_counts())

if __name__ == "__main__":
    inspect_university_dataset()
