"""
Script to launch EduPredict AI FastAPI Backend Server on port 8000
"""

import uvicorn
import os
import sys

# Ensure backend package is in pythonpath
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    print("=" * 75)
    print("STARTING EduPredict AI BACKEND SERVER (FastAPI + Uvicorn)")
    print("SAPTHAGIRI NPS UNIVERSITY, BENGALURU")
    print("Docs available at: http://localhost:8000/docs")
    print("=" * 75)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
