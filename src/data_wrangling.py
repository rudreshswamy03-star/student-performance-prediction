"""
Module: data_wrangling.py
Purpose: Data cleaning, wrangling, validation, and preprocessing pipeline.
Course: Data Mining and Data Wrangling
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def load_and_wrangle_data(filepath: str = "dataset/student-mat.csv") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Loads raw student-mat.csv, inspects anomalies, checks missing values,
    checks duplicates, and prepares the wrangled dataframe.
    """
    # 1. Load dataset with semicolon delimiter
    df = pd.read_csv(filepath, sep=';')
    
    # 2. Audit initial state
    initial_rows = len(df)
    missing_counts = df.isnull().sum().to_dict()
    total_missing = sum(missing_counts.values())
    
    # 3. Check and drop duplicate records
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        df = df.drop_duplicates()
        
    # 4. Data validation: ensure grades are within [0, 20]
    for col in ['G1', 'G2', 'G3']:
        df[col] = df[col].clip(lower=0, upper=20)
        
    # 5. Outlier inspection on absences (e.g. absences > 50 are extreme)
    q1 = df['absences'].quantile(0.25)
    q3 = df['absences'].quantile(0.75)
    iqr = q3 - q1
    absence_upper_bound = q3 + 1.5 * iqr
    outlier_absences_count = int((df['absences'] > absence_upper_bound).sum())

    wrangling_summary = {
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "total_columns": df.shape[1],
        "total_missing_values": int(total_missing),
        "duplicate_records": int(duplicates_count),
        "outlier_absences_count": outlier_absences_count,
        "absence_iqr_threshold": float(absence_upper_bound)
    }
    
    return df, wrangling_summary

def get_feature_columns() -> Tuple[list, list]:
    """
    Returns lists of categorical and numerical features used for model training.
    Target variable G3 is excluded.
    G1 and G2 are retained as previous exam marks as requested.
    """
    categorical_cols = [
        'school', 'sex', 'address', 'famsize', 'Pstatus',
        'Mjob', 'Fjob', 'reason', 'guardian',
        'schoolsup', 'famsup', 'paid', 'activities',
        'nursery', 'higher', 'internet', 'romantic'
    ]
    
    numerical_cols = [
        'age', 'Medu', 'Fedu', 'traveltime', 'studytime',
        'failures', 'famrel', 'freetime', 'goout',
        'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2'
    ]
    
    return categorical_cols, numerical_cols

def build_preprocessor() -> ColumnTransformer:
    """
    Builds a Scikit-Learn ColumnTransformer pipeline:
    - Standardizes numerical variables (zero mean, unit variance)
    - One-hot encodes categorical variables without target leakage
    """
    categorical_cols, numerical_cols = get_feature_columns()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ]
    )
    return preprocessor

def prepare_train_test_split(
    df: pd.DataFrame, 
    test_size: float = 0.20, 
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Splits features and target G3 into 80% train and 20% test sets.
    """
    categorical_cols, numerical_cols = get_feature_columns()
    feature_cols = categorical_cols + numerical_cols
    
    X = df[feature_cols].copy()
    y = df['G3'].copy()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    df, summary = load_and_wrangle_data()
    print("Wrangling Summary:", summary)
    X_train, X_test, y_train, y_test = prepare_train_test_split(df)
    print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
