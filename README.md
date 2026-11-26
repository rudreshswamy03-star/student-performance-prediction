# 🎓 EduPredict AI: Student Academic Performance Analysis and Prediction System
### Sapthagiri NPS University, Bengaluru, Karnataka, India
#### Department of Computer Science and Engineering | Academic Year 2026–2027

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Dashboard](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-indigo.svg)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An end-to-end Machine Learning and Educational Data Mining (EDM) decision-support system designed for undergraduate engineering students (5th Semester B.E.) at Sapthagiri NPS University, Bengaluru. The system analyzes continuous internal assessments, attendance patterns, study habits, and backlog history to forecast final semester performance and deliver early-warning academic guidance.

---

## 📌 Table of Contents
- [Institutional Context & Overview](#-institutional-context--overview)
- [Problem Statement](#-problem-statement)
- [Key Features & Capabilities](#-key-features--capabilities)
- [Core Academic Subjects (5th Semester)](#-core-academic-subjects-5th-semester)
- [Dataset Specifications & Disclaimer](#-dataset-specifications--disclaimer)
- [System Architecture & Folder Structure](#-system-architecture--folder-structure)
- [📱 Mobile Application (React Native / Expo)](#-mobile-application-react-native--expo)
- [⚡ FastAPI Backend Service](#-fastapi-backend-service)
- [Machine Learning Benchmark Results](#-machine-learning-benchmark-results)
- [Early Warning System Protocols](#-early-warning-system-protocols)
- [Installation & Quick Start](#-installation--quick-start)
- [Future Enhancements](#-future-enhancements)
- [Academic Documentation](#-academic-documentation)

---

## 🏛 Institutional Context & Overview

- **Institution:** Sapthagiri NPS University, Bengaluru, Karnataka, India
- **Department:** Department of Computer Science and Engineering
- **Program:** Bachelor of Engineering (B.E.), 5th Semester
- **Course:** Data Mining and Data Wrangling
- **Academic Year:** 2026–2027
- **Developer:** Rudresh Swamy

Traditional academic evaluations are post-hoc—educators identify struggling students only after end-semester examinations conclude. **EduPredict AI** bridges this critical gap by transforming formative Continuous Internal Evaluation (CIE) data, attendance records, and learning habits into an **Early Academic Warning System**.

---

## 🎯 Problem Statement

In engineering degree programs, academic decline is rarely caused by a single factor. Complex interactions between:
1. Low attendance and absenteeism (< 75% university regulation threshold)
2. Active backlogs dividing examination focus
3. Inadequate daily self-study hours (< 2.5 hrs/day)
4. Specific conceptual weaknesses in rigorous subjects (e.g., Mathematics, Data Structures & Algorithms)

lead to poor semester clearance rates. EduPredict AI equips department heads, mentors, and counselors with real-time empirical forecasting to trigger proactive remedial tutoring before final examinations take place.

---

## 🚀 Key Features & Capabilities

1. **Executive University Dashboard:** Live KPI metrics (Cohort Size, Average CGPA, Attendance, Daily Study Hours, At-Risk Counts) and dynamic Plotly visualizations.
2. **Dedicated Dataset Explorer:** Multi-attribute filtering by Section (A, B, C), Gender, and Performance Tier, plus complete CSV export.
3. **Exploratory Data Analysis (EDA):** Correlation heatmaps, subject-wise grade variance distributions, and attendance impact analysis.
4. **Machine Learning Benchmarking:** Automated cross-validation across **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor** with zero target leakage.
5. **Interactive Performance Predictor:** Form interface accepting subject marks, attendance, and study habits to forecast final scores (0–100) and performance tiers.
6. **Early Academic Warning System:** Automated risk stratification (Low, Medium, High Risk) based on attendance and backlog thresholds, complete with downloadable mentor rosters.
7. **Individual Student Profiles:** Full 360-degree student cards with subject mark radar/bar charts comparing individual scores against the cohort mean.

---

## 📚 Core Academic Subjects (5th Semester)

The system continuously models performance across all six core curriculum subjects:
1. **Mathematics** (Advanced Engineering Mathematics & Discrete Structures)
2. **Data Structures and Algorithms**
3. **Database Management Systems**
4. **Operating Systems**
5. **Computer Networks**
6. **Data Mining and Data Wrangling**

---

## 📊 Dataset Specifications & Disclaimer

- **Cohort Size:** 300 engineering students (Unique IDs: `SNP001` to `SNP300`)
- **Format:** 28 structured attributes including demographics, attendance, study habits, backlogs, and subject marks.
- **Target Variables:**
  - `Final_Score`: Continuous performance score (0.0 to 100.0)
  - `Predicted_Performance_Category`:
    * **Excellent:** 85.0 – 100.0
    * **Very Good:** 70.0 – 84.9
    * **Good:** 60.0 – 69.9
    * **Average:** 50.0 – 59.9
    * **Needs Improvement:** < 50.0
- ⚠️ **Academic Disclaimer:** This dataset is a synthesized simulation designed exclusively for academic demonstration and machine learning benchmarking for Sapthagiri NPS University. It does not contain private or actual student records.

---

## 📁 System Architecture & Folder Structure

```text
student-performance-prediction/
│
├── dataset/
│   ├── university_students.csv      # 300-student Sapthagiri NPS University cohort
│   ├── student-mat.csv              # Archive benchmark dataset
│   └── student.txt                  # Original dataset documentation
│
├── docs/                            # College Submission Deliverables
│   ├── Academic_Project_Report.md   # 19-section full college project report
│   └── Viva_and_Presentation_Guide.md # Top viva Q&As & presentation outline
│
├── model/                           # Serialized Model Artifacts
│   ├── best_model.joblib            # Serialized winning pipeline (ColumnTransformer + Model)
│   └── model_metrics.json           # Real validation metrics & feature importances
│
├── notebooks/                       # Jupyter Notebook experiment directory (.gitkeep)
│
├── src/                             # Modular Python Source Modules
│   ├── data_wrangling.py            # Data cleaning, outlier checks & Scikit-Learn pipeline
│   ├── demo_cases.py                # Multi-profile batch inference demonstration
│   ├── generate_university_data.py  # Realistic 300-student synthetic data generator
│   ├── inspect_dataset.py           # Dataset sanity check and preliminary inspection
│   ├── predict.py                   # Standalone inference engine and counseling rules
│   └── train_models.py              # Model benchmarking, training & Joblib serialization
│
├── backend/                         # ⚡ FastAPI High-Performance Backend
│   ├── app/
│   │   ├── routers/                 # Modular API endpoints (auth, students, predict, warning)
│   │   ├── auth.py                  # JWT authentication & role-based access control
│   │   ├── config.py                # University branding & settings
│   │   ├── database.py              # SQLite storage & seed users
│   │   └── main.py                  # FastAPI core application & CORS middleware
│   └── run_server.py                # Standalone Uvicorn launcher (Port 8000)
│
├── mobile/                          # 📱 React Native / Expo Mobile Application
│   ├── assets/                      # University branded icons and splash screens
│   ├── src/
│   │   ├── components/              # Buttons, Cards, Badges
│   │   ├── context/                 # AuthContext & Session management
│   │   ├── navigation/              # Bottom Tabs & Stack navigation
│   │   ├── screens/                 # Splash, Onboarding, Login, Home, Academics, Predictor, Warning
│   │   ├── services/                # REST API client connecting to FastAPI
│   │   └── theme/                   # University color palette & typography
│   ├── App.tsx                      # Root component
│   ├── app.json                     # Android & iOS bundle configuration
│   └── package.json                 # Mobile dependencies
│
├── app.py                           # Full Streamlit interactive university web dashboard
├── desktop_app.py                   # Windows Native Edge App / Tkinter desktop interface
├── main.py                          # Master execution runner (runs full pipeline end-to-end)
├── run.bat                          # One-click Windows batch launcher
├── requirements.txt                 # Project library dependencies (FastAPI, Scikit-Learn, Streamlit)
├── .gitignore                       # Clean Git exclusion rules
└── README.md                        # Project documentation
```

---

## 📱 Mobile Application (React Native / Expo)

EduPredict AI includes a fully-featured, cross-platform mobile application for Android and iOS:
- **Splash & University Onboarding:** 4-step walkthrough emphasizing student success and early intervention.
- **Role-Based Authentication:** Dedicated portals for **Student**, **Faculty**, and **Administrator** with One-Touch Demo logins.
- **Interactive AI Performance Predictor:** Direct mobile inference against the trained Scikit-Learn machine learning model.
- **Early Academic Warning System (EAWS):** Filterable risk roster with counseling protocol triggers.
- **6 Core Subjects Audit:** Real-time CIE-1, CIE-2, and attendance tracking for 5th semester courses.
- **Android APK Build:** Ready for standalone APK generation via Expo Application Services (`eas build -p android --profile preview`).

For detailed mobile instructions, see [`mobile/README.md`](mobile/README.md).

---

## ⚡ FastAPI Backend Service

The mobile application is powered by a dedicated high-performance **FastAPI** backend:
- **FastAPI Core:** Automatic OpenAPI / Swagger UI interactive documentation at `http://localhost:8000/docs`.
- **Machine Learning Endpoint (`POST /api/predict`):** Direct real-time inference using the trained `best_model.joblib`.
- **Early Warning Endpoint (`GET /api/early-warning`):** Real-time risk categorization and intervention roster.
- **Role-Based Access Control (RBAC):** Token authentication protecting student, faculty, and administrative routes.

---

## 📈 Machine Learning Benchmark Results

All models were evaluated on the held-out **20% unseen test partition** ($N=60$, `random_state=42`):

| Algorithm | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | Root Mean Squared Error (RMSE) | $R^2$ Score (Variance Explained) |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression** | **2.6087** | **11.3731** | **3.3724** | **0.9277 (92.8%)** 🏆 |
| **Random Forest Regressor** | 3.0100 | 15.1239 | 3.8889 | 0.9039 (90.4%) |
| **Decision Tree Regressor** | 4.4868 | 32.7749 | 5.7249 | 0.7918 (79.2%) |

> **Selection:** **Linear Regression** emerged as the winning model, capturing the strong continuous additive relationships of formative assessments with lowest validation error ($\text{RMSE} = 3.3724$).

### Top Predictive Factors:
1. **Six-Subject Formative Marks:** Direct continuous indicators of syllabus mastery.
2. **Previous CGPA:** Longitudinal stability factor across semesters 1–4.
3. **Attendance Percentage:** High attendance prevents knowledge fragmentation.
4. **Active Backlogs:** Primary negative predictor and indicator of academic distress.

---

## 🚨 Early Warning System Protocols

| Tier | Empirical Trigger Criteria | Action Protocol |
| :--- | :--- | :--- |
| **🔴 High Risk** | Predicted Score $< 50$, Attendance $< 65\%$, or $\ge 3$ Backlogs | Immediate parent-mentor conference, remedial class assignment, weekly progress monitoring. |
| **🟡 Medium Risk** | Predicted Score $50 - 59$, Attendance $65 - 74\%$, or $2$ Backlogs | Faculty mentor counseling, assignment submission recovery plan, peer study groups. |
| **🟢 Low Risk** | Predicted Score $\ge 60$, Attendance $\ge 75\%$, $\le 1$ Backlog | Standard academic tracking; encouragement for technical hackathons and research mini-projects. |

---

## 🚀 Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rudreshswamy03-star/student-performance-prediction.git
cd student-performance-prediction
```

### 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Master Script (CLI Mode)
```bash
python main.py
```
*(On Windows, you can also double-click `run.bat`)*

### 4. Launch the Interactive Web Dashboard
```bash
python -m streamlit run app.py
```
Then navigate to: **`http://localhost:8501`**

---

## 🔮 Future Enhancements

- [ ] Automated email/SMS alert dispatch to parents when attendance drops below 75%.
- [ ] Integration with university Enterprise Resource Planning (ERP) databases.
- [ ] Longitudinal tracking spanning semesters 6, 7, and 8.

---

## 📄 Academic Documentation

- 📖 [Comprehensive Academic Project Report (19 Sections)](docs/Academic_Project_Report.md)
- 🎓 [Viva Preparation & Project Presentation Guide](docs/Viva_and_Presentation_Guide.md)

---

## 👨‍💻 Author

- **Name:** Rudresh Swamy
- **Institution:** Sapthagiri NPS University, Bengaluru
- **Department:** Computer Science and Engineering