"""
Module: inspect_dataset.py
Purpose: Preliminary inspection of the raw student-mat.csv dataset.
Course: Data Mining and Data Wrangling
"""

import pandas as pd
import os

def inspect_student_dataset(filepath: str = "dataset/student-mat.csv") -> None:
    """
    Loads and inspects the raw student-mat.csv file.
    Note: The UCI dataset uses semicolon (;) as the delimiter, not commas!
    """
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found at {filepath}. Please run download_data.py first.")
        return

    print("=" * 70)
    print("STEP 1: LOADING DATASET")
    print("=" * 70)
    # Important: sep=';' is required because the raw dataset is semicolon-delimited
    df = pd.read_csv(filepath, sep=';')
    print(f"Dataset successfully loaded. Shape: {df.shape[0]} rows, {df.shape[1]} columns.\n")

    print("=" * 70)
    print("STEP 2: FIRST 5 RECORDS (HEAD)")
    print("=" * 70)
    print(df.head())

    print("\n" + "=" * 70)
    print("STEP 3: DATA TYPES & NON-NULL COUNTS")
    print("=" * 70)
    df.info()

    print("\n" + "=" * 70)
    print("STEP 4: SUMMARY STATISTICS (NUMERICAL COLUMNS)")
    print("=" * 70)
    print(df.describe())

    print("\n" + "=" * 70)
    print("STEP 5: TARGET VARIABLE ('G3') DISTRIBUTION")
    print("=" * 70)
    print("Summary of Final Grade (G3):")
    print(df['G3'].describe())
    print("\nGrade Value Counts:")
    print(df['G3'].value_counts().sort_index())

if __name__ == "__main__":
    inspect_student_dataset()
