"""
Module: train_models.py
Purpose: Benchmark and evaluate Linear Regression, Decision Tree, and Random Forest
         on Sapthagiri NPS University student data, then serialize the best model.
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_wrangling import (
    load_and_wrangle_data,
    prepare_train_test_split,
    build_preprocessor,
    get_feature_columns
)

def train_and_evaluate_models():
    os.makedirs("model", exist_ok=True)

    # 1. Load wrangled university dataset and split 80/20
    df, wrangling_summary = load_and_wrangle_data()
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, test_size=0.20, random_state=42)

    print(f"[INFO] Cohort: {wrangling_summary['institution']}")
    print(f"[INFO] Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    # 2. Candidate Regression Algorithms
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, min_samples_split=6, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=120, max_depth=10, min_samples_split=4, random_state=42)
    }

    results = {}
    fitted_pipelines = {}

    for name, model in models.items():
        print(f"\n[TRAINING] Training {name}...")

        pipeline = Pipeline(steps=[
            ('preprocessor', build_preprocessor()),
            ('regressor', model)
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)

        results[name] = {
            "MAE": round(float(mae), 4),
            "MSE": round(float(mse), 4),
            "RMSE": round(float(rmse), 4),
            "R2": round(float(r2), 4)
        }
        fitted_pipelines[name] = pipeline

        print(f" -> {name} | MAE: {mae:.4f} | MSE: {mse:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f}")

    # 3. Best Model Selection (lowest RMSE / highest R2)
    best_model_name = min(results, key=lambda k: results[k]["RMSE"])
    best_pipeline = fitted_pipelines[best_model_name]
    print(f"\n[SELECTION] Best Performing Model: {best_model_name} (RMSE: {results[best_model_name]['RMSE']})")

    # 4. Feature Importance Extraction
    cat_cols, num_cols = get_feature_columns()
    preprocessor = best_pipeline.named_steps['preprocessor']
    cat_encoder = preprocessor.named_transformers_['cat']
    encoded_cat_names = list(cat_encoder.get_feature_names_out(cat_cols))
    all_feature_names = num_cols + encoded_cat_names

    regressor = best_pipeline.named_steps['regressor']
    feature_importance_list = []

    if hasattr(regressor, 'feature_importances_'):
        importances = regressor.feature_importances_
        for feat, imp in zip(all_feature_names, importances):
            feature_importance_list.append({"feature": feat, "importance": round(float(imp), 5)})
        feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)
    elif hasattr(regressor, 'coef_'):
        coefs = regressor.coef_
        for feat, coef in zip(all_feature_names, coefs):
            feature_importance_list.append({"feature": feat, "importance": round(float(abs(coef)), 5)})
        feature_importance_list.sort(key=lambda x: x["importance"], reverse=True)

    # 5. Serialize best model with Joblib
    best_model_path = os.path.join("model", "best_model.joblib")
    joblib.dump(best_pipeline, best_model_path)
    print(f"[SAVED] Serialized pipeline saved to: {best_model_path}")

    # 6. Save metadata to JSON
    metadata = {
        "institution": wrangling_summary["institution"],
        "department": wrangling_summary["department"],
        "academic_year": wrangling_summary["academic_year"],
        "semester": wrangling_summary["current_semester"],
        "best_model_name": best_model_name,
        "metrics": results,
        "feature_importances": feature_importance_list[:15],
        "wrangling_summary": wrangling_summary
    }
    metrics_path = os.path.join("model", "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"[SAVED] Evaluation metrics saved to: {metrics_path}")

    return metadata

if __name__ == "__main__":
    train_and_evaluate_models()
