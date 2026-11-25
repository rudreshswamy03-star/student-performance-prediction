"""
Module: train_models.py
Purpose: Train, evaluate, compare ML models (Linear Regression, Decision Tree, Random Forest)
         and serialize the best performing pipeline using Joblib.
Course: Data Mining and Data Wrangling
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_wrangling import (
    load_and_wrangle_data, 
    prepare_train_test_split, 
    build_preprocessor,
    get_feature_columns
)

def train_and_evaluate_models():
    os.makedirs("model", exist_ok=True)
    
    # 1. Load wrangled data and split into 80% train and 20% test
    df, wrangling_summary = load_and_wrangle_data()
    X_train, X_test, y_train, y_test = prepare_train_test_split(df, test_size=0.20, random_state=42)
    
    print(f"[INFO] Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    
    # 2. Define the Candidate Regression Algorithms
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=5, min_samples_split=5, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=8, min_samples_split=4, random_state=42)
    }
    
    results = {}
    fitted_pipelines = {}
    
    for name, model in models.items():
        print(f"\n[TRAINING] Training {name}...")
        
        # Build unified pipeline (preprocessor + regressor) to strictly prevent data leakage
        pipeline = Pipeline(steps=[
            ('preprocessor', build_preprocessor()),
            ('regressor', model)
        ])
        
        # Train solely on X_train, y_train
        pipeline.fit(X_train, y_train)
        
        # Predict on unseen test set
        y_pred = pipeline.predict(X_test)
        
        # Calculate evaluation metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results[name] = {
            "MAE": round(float(mae), 4),
            "RMSE": round(float(rmse), 4),
            "R2": round(float(r2), 4)
        }
        fitted_pipelines[name] = pipeline
        
        print(f" -> {name} | MAE: {mae:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f}")
        
    # 3. Determine the Best Model based on Lowest RMSE (and Highest R²)
    best_model_name = min(results, key=lambda k: results[k]["RMSE"])
    best_pipeline = fitted_pipelines[best_model_name]
    print(f"\n[SELECTION] Best Performing Model: {best_model_name} (RMSE: {results[best_model_name]['RMSE']})")
    
    # 4. Extract Feature Importances / Coefficients
    categorical_cols, numerical_cols = get_feature_columns()
    preprocessor = best_pipeline.named_steps['preprocessor']
    
    # Get encoded feature names
    cat_encoder = preprocessor.named_transformers_['cat']
    encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_cols))
    all_feature_names = numerical_cols + encoded_cat_names
    
    feature_importance_list = []
    regressor = best_pipeline.named_steps['regressor']
    
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

    # 5. Save the best pipeline using Joblib
    best_model_path = os.path.join("model", "best_model.joblib")
    joblib.dump(best_pipeline, best_model_path)
    print(f"[SAVED] Saved best pipeline to: {best_model_path}")
    
    # 6. Save metrics and metadata to JSON
    metadata = {
        "best_model_name": best_model_name,
        "metrics": results,
        "feature_importances": feature_importance_list[:15],
        "wrangling_summary": wrangling_summary
    }
    metrics_path = os.path.join("model", "model_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"[SAVED] Saved model metrics to: {metrics_path}")

    return metadata

if __name__ == "__main__":
    train_and_evaluate_models()
