"""
================================================================================
FastAPI Backend Application Entry Point
EduPredict AI: Student Academic Performance Analysis and Prediction System
Institution: Sapthagiri NPS University, Bengaluru
================================================================================
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_database
from .routers.auth_router import router as auth_router
from .routers.students_router import router as students_router
from .routers.prediction_router import router as prediction_router
from .routers.academics_router import router as academics_router
from .routers.warning_router import router as warning_router
from .routers.faculty_router import faculty_router, admin_router

app = FastAPI(
    title="EduPredict AI API - Sapthagiri NPS University",
    description="Backend REST API serving the EduPredict AI Mobile & Web Applications with Machine Learning Prediction and Academic Analytics.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Mobile App and Web App connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_database()
    print("[BACKEND] EduPredict AI Database and ML Services initialized.")

# Mount Routers
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(prediction_router)
app.include_router(academics_router)
app.include_router(warning_router)
app.include_router(faculty_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {
        "system": "EduPredict AI Mobile Backend",
        "institution": "Sapthagiri NPS University, Bengaluru",
        "department": "Computer Science and Engineering",
        "academic_year": "2026–2027",
        "version": "2.0.0",
        "status": "Operational",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
