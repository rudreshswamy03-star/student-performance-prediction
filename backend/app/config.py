"""
Configuration settings for EduPredict AI Backend API
Sapthagiri NPS University, Bengaluru
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "university_students.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "best_model.joblib")
METRICS_PATH = os.path.join(BASE_DIR, "model", "model_metrics.json")
DB_PATH = os.path.join(BASE_DIR, "backend", "edupredict.db")

SECRET_KEY = "sapthagiri_nps_university_edupredict_super_secret_jwt_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

INSTITUTION_NAME = "Sapthagiri NPS University"
LOCATION = "Bengaluru, Karnataka, India"
DEPARTMENT = "Department of Computer Science and Engineering"
ACADEMIC_YEAR = "2026–2027"
SEMESTER = "5th Semester"
