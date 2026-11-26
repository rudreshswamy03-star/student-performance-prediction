"""
Module: data_wrangling.py
Purpose: Data cleaning, wrangling, validation, and preprocessing pipeline for
         Sapthagiri NPS University Student Academic Performance System.
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_and_wrangle_data(filepath: str = "dataset/university_students.csv") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Loads raw university student cohort data, inspects data types, audits missing values
    and duplicate records, validates range constraints, and computes outlier bounds.
    """
    if not os.path.exists(filepath):
        from generate_university_data import save_university_dataset
        filepath = save_university_dataset(filepath)

    df = pd.read_csv(filepath)

    initial_rows = len(df)
    missing_counts = df.isnull().sum().to_dict()
    total_missing = int(sum(missing_counts.values()))
    duplicates_count = int(df.duplicated(subset=['Student_ID']).sum())

    if duplicates_count > 0:
        df = df.drop_duplicates(subset=['Student_ID'])

    # Range and sanity constraints
    df['Previous_CGPA'] = df['Previous_CGPA'].clip(lower=0.0, upper=10.0)
    df['Attendance_Percentage'] = df['Attendance_Percentage'].clip(lower=0.0, upper=100.0)
    df['Assignment_Completion_Percentage'] = df['Assignment_Completion_Percentage'].clip(lower=0.0, upper=100.0)
    df['Final_Score'] = df['Final_Score'].clip(lower=0.0, upper=100.0)

    subject_cols = [
        'Marks_Mathematics', 'Marks_DSA', 'Marks_DBMS',
        'Marks_OS', 'Marks_CN', 'Marks_DMW'
    ]
    for col in subject_cols:
        df[col] = df[col].clip(lower=0.0, upper=100.0)

    # IQR Outlier Analysis on Absences and Backlogs
    q1_abs = df['Absence_Days'].quantile(0.25)
    q3_abs = df['Absence_Days'].quantile(0.75)
    iqr_abs = q3_abs - q1_abs
    absence_upper_bound = float(q3_abs + 1.5 * iqr_abs)
    outlier_absences_count = int((df['Absence_Days'] > absence_upper_bound).sum())

    q1_cgpa = df['Previous_CGPA'].quantile(0.25)
    q3_cgpa = df['Previous_CGPA'].quantile(0.75)
    iqr_cgpa = q3_cgpa - q1_cgpa
    cgpa_lower_bound = float(max(0.0, q1_cgpa - 1.5 * iqr_cgpa))
    cgpa_outliers_count = int((df['Previous_CGPA'] < cgpa_lower_bound).sum())

    summary = {
        "institution": "Sapthagiri NPS University, Bengaluru",
        "department": "Computer Science and Engineering",
        "academic_year": "2026–2027",
        "current_semester": "5th Semester",
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "total_columns": df.shape[1],
        "total_missing_values": total_missing,
        "duplicate_records": duplicates_count,
        "outlier_absences_count": outlier_absences_count,
        "absence_iqr_threshold": round(absence_upper_bound, 1),
        "cgpa_outliers_count": cgpa_outliers_count,
        "average_cgpa": round(float(df['Previous_CGPA'].mean()), 2),
        "average_attendance": round(float(df['Attendance_Percentage'].mean()), 1),
        "average_final_score": round(float(df['Final_Score'].mean()), 1)
    }

    return df, summary

def get_feature_columns() -> Tuple[List[str], List[str]]:
    """
    Returns lists of categorical and numerical feature names for machine learning.
    Target variable 'Final_Score' and identifier metadata are excluded.
    """
    categorical_cols = [
        'Section',
        'Gender',
        'Previous_Semester_Performance',
        'Extracurricular_Participation'
    ]

    numerical_cols = [
        'Age',
        'Previous_CGPA',
        'Attendance_Percentage',
        'Absence_Days',
        'Daily_Study_Hours',
        'Weekly_Library_Hours',
        'Online_Learning_Hours',
        'Assignment_Completion_Percentage',
        'Internal_Assessment_Marks',
        'Backlogs',
        'Marks_Mathematics',
        'Marks_DSA',
        'Marks_DBMS',
        'Marks_OS',
        'Marks_CN',
        'Marks_DMW'
    ]

    return categorical_cols, numerical_cols

def build_preprocessor() -> ColumnTransformer:
    """
    Constructs a ColumnTransformer pipeline:
    - StandardScaler for numerical student metrics
    - OneHotEncoder (drop='first') for categorical student background features
    """
    cat_cols, num_cols = get_feature_columns()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_cols)
        ]
    )
    return preprocessor

def prepare_train_test_split(
    df: pd.DataFrame,
    test_size: float = 0.20,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Partitions features and target 'Final_Score' into 80% train and 20% test sets.
    """
    cat_cols, num_cols = get_feature_columns()
    feature_cols = cat_cols + num_cols

    X = df[feature_cols].copy()
    y = df['Final_Score'].copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df, summary = load_and_wrangle_data()
    print("Wrangling Summary:", summary)
    X_train, X_test, y_train, y_test = prepare_train_test_split(df)
    print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
