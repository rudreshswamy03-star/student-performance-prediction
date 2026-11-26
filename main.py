"""
================================================================================
SAPTHAGIRI NPS UNIVERSITY, BENGALURU
DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (2026-2027)
COURSE: Data Mining and Data Wrangling (5th Semester)
APPLICATION: EduPredict AI - Student Academic Performance System
MASTER RUNNER: main.py
================================================================================
"""

import sys
import os
import webbrowser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

def banner():
    print("*" * 80)
    print("                SAPTHAGIRI NPS UNIVERSITY, BENGALURU")
    print("             DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    print("               EduPredict AI - Academic Performance System")
    print("                    DATA MINING & DATA WRANGLING CAPSTONE")
    print("*" * 80)

def step_1_check_dataset():
    print("\n[STEP 1/5] Verifying University Cohort Dataset...")
    data_path = os.path.join("dataset", "university_students.csv")
    if not os.path.exists(data_path):
        print("  -> Dataset missing. Generating 300-student cohort dataset for Sapthagiri NPS University...")
        from generate_university_data import save_university_dataset
        save_university_dataset(data_path)
    else:
        print(f"  -> Verified university dataset located at '{data_path}'.")

def step_2_wrangle_data():
    print("\n[STEP 2/5] Performing Data Wrangling & Outlier Checks...")
    from data_wrangling import load_and_wrangle_data
    df, summary = load_and_wrangle_data()
    print(f"  -> Institution              : {summary['institution']}")
    print(f"  -> Department & Cohort      : {summary['department']} ({summary['current_semester']})")
    print(f"  -> Total Student Records    : {summary['final_rows']}")
    print(f"  -> Total Attributes         : {summary['total_columns']}")
    print(f"  -> Missing Values Detected  : {summary['total_missing_values']}")
    print(f"  -> Duplicate IDs Detected   : {summary['duplicate_records']}")
    print(f"  -> Average Previous CGPA    : {summary['average_cgpa']}")
    print(f"  -> Average Attendance       : {summary['average_attendance']}%")
    print(f"  -> Outlier Absences (IQR)   : {summary['outlier_absences_count']} records (> {summary['absence_iqr_threshold']:.1f} days)")

def step_3_train_models():
    print("\n[STEP 3/5] Benchmarking Machine Learning Algorithms...")
    from train_models import train_and_evaluate_models
    metadata = train_and_evaluate_models()

    print("\n  ================================================================")
    print("  MODEL EVALUATION BENCHMARK RESULTS (Test Set: 20%):")
    print("  ================================================================")
    print("  {:<22} | {:<8} | {:<8} | {:<8} | {:<8}".format("Algorithm", "MAE", "MSE", "RMSE", "R² Score"))
    print("  " + "-" * 66)
    for model_name, metrics in metadata["metrics"].items():
        print("  {:<22} | {:<8.4f} | {:<8.4f} | {:<8.4f} | {:<8.4f}".format(
            model_name, metrics["MAE"], metrics["MSE"], metrics["RMSE"], metrics["R2"]
        ))
    print("  " + "-" * 66)
    print(f"  [WINNER] Selected Best Model: {metadata['best_model_name']}")
    print("  ================================================================")

def step_4_inference_demo():
    print("\n[STEP 4/5] Executing Academic Risk & Prediction Demonstration...")
    from demo_cases import run_demonstration
    run_demonstration()

def step_5_launch_webapp():
    print("\n[STEP 5/5] Streamlit Web Dashboard Status...")
    web_url = "http://localhost:8501"
    print(f"  -> Web Dashboard is configured for: {web_url}")
    print("  -> Launching browser...")
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
    print("       ALL MODULES EXECUTED SUCCESSFULLY! SYSTEM IS READY.")
    print("*" * 80)

if __name__ == "__main__":
    main()
