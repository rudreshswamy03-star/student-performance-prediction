"""
================================================================================
PROJECT: Student Performance Prediction Using Data Mining
SUBJECT: Data Mining and Data Wrangling
ENTRY POINT: main.py
================================================================================
"""

import sys
import os
import subprocess
import webbrowser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Force UTF-8 stdout encoding for clean Windows console output
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def banner():
    print("*" * 80)
    print("       STUDENT PERFORMANCE PREDICTION USING DATA MINING & WRANGLING")
    print("                       ACADEMIC CAPSTONE PROJECT")
    print("*" * 80)

def step_1_check_dataset():
    print("\n[STEP 1/5] Checking Dataset Availability...")
    data_path = os.path.join("dataset", "student-mat.csv")
    if not os.path.exists(data_path):
        print("  -> Dataset missing. Downloading from UCI Machine Learning Repository...")
        from src.download_data import download_and_extract_dataset
        download_and_extract_dataset()
    else:
        print(f"  -> Found verified dataset at '{data_path}'.")

def step_2_wrangle_data():
    print("\n[STEP 2/5] Running Data Wrangling & Integrity Checks...")
    from src.data_wrangling import load_and_wrangle_data
    df, summary = load_and_wrangle_data()
    print(f"  -> Total Student Records    : {summary['final_rows']}")
    print(f"  -> Total Features           : {summary['total_columns']}")
    print(f"  -> Missing Values Detected  : {summary['total_missing_values']}")
    print(f"  -> Duplicate Records Found  : {summary['duplicate_records']}")
    print(f"  -> Absence Outliers (IQR)   : {summary['outlier_absences_count']} records (> {summary['absence_iqr_threshold']:.1f} days)")

def step_3_train_models():
    print("\n[STEP 3/5] Benchmarking Machine Learning Algorithms...")
    from src.train_models import train_and_evaluate_models
    metadata = train_and_evaluate_models()
    
    print("\n  ================================================================")
    print("  MODEL EVALUATION BENCHMARK RESULTS (Test Set: 20%):")
    print("  ================================================================")
    print("  {:<25} | {:<10} | {:<10} | {:<10}".format("Algorithm", "MAE", "RMSE", "R² Score"))
    print("  " + "-" * 62)
    for model_name, metrics in metadata["metrics"].items():
        print("  {:<25} | {:<10.4f} | {:<10.4f} | {:<10.4f}".format(
            model_name, metrics["MAE"], metrics["RMSE"], metrics["R2"]
        ))
    print("  " + "-" * 62)
    print(f"  [WINNER] Selected Best Model: {metadata['best_model_name']}")
    print("  ================================================================")

def step_4_inference_demo():
    print("\n[STEP 4/5] Executing Prediction Inference Demonstration...")
    from src.demo_cases import run_demonstration
    run_demonstration()

def step_5_launch_webapp():
    print("\n[STEP 5/5] Streamlit Web Dashboard Status...")
    web_url = "http://localhost:8501"
    print(f"  -> Web Dashboard is live and accessible at: {web_url}")
    print("  -> Opening browser now...")
    try:
        webbrowser.open(web_url)
    except Exception as e:
        print(f"  -> Could not automatically open browser: {e}. Please visit {web_url} manually.")

def main():
    banner()
    step_1_check_dataset()
    step_2_wrangle_data()
    step_3_train_models()
    step_4_inference_demo()
    step_5_launch_webapp()
    print("\n" + "*" * 80)
    print("       ALL MODULES EXECUTED SUCCESSFULLY! PROJECT IS READY.")
    print("*" * 80)

if __name__ == "__main__":
    main()
