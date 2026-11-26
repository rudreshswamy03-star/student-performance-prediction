# ACADEMIC PROJECT REPORT

## PROJECT TITLE:
### **EduPredict AI: Student Academic Performance Analysis and Prediction System**
#### **Sapthagiri NPS University, Bengaluru, Karnataka, India**
#### **Department of Computer Science and Engineering | Academic Year 2026–2027**

---

### **1. ABSTRACT**
Student academic performance prediction is a critical challenge in Educational Data Mining (EDM). Early identification of at-risk students empowers faculty mentors and academic counselors to offer timely remedial interventions, preventing course dropouts and semester backlogs. This project designs, evaluates, and deploys an end-to-end Machine Learning decision-support system tailored for undergraduate engineering students ($N=300$, 5th Semester B.E.) at Sapthagiri NPS University, Bengaluru. Using structured data wrangling, missing-value audits, duplicate filtering, IQR-based outlier diagnostics, and a Scikit-Learn `ColumnTransformer` preprocessing pipeline (`StandardScaler` and `OneHotEncoder`), we benchmark three core algorithms: **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor**. Evaluated on the held-out 20% test partition ($N=60$), **Linear Regression** achieved the best overall generalization, obtaining a **Mean Absolute Error (MAE) of 2.6087**, a **Root Mean Squared Error (RMSE) of 3.3724**, and an **$R^2$ score of 0.9277**, explaining over 92.7% of the variance in final semester examination scores. The trained pipeline is serialized using Joblib and served via a modern, interactive Streamlit web application.

---

### **2. INTRODUCTION**
Higher education institutions continuously seek proactive mechanisms to enhance student graduation rates and academic mastery. Traditional evaluation models assess student performance only after summative end-semester examinations conclude, eliminating any opportunity for corrective instruction. Educational Data Mining (EDM) bridges this gap by discovering multi-factorial relationships among continuous internal evaluations (CIE), attendance records, daily study hours, active backlogs, and academic history across six 5th-semester engineering subjects.

---

### **3. PROBLEM STATEMENT**
In rigorous undergraduate engineering programs, academic decline is seldom driven by a lack of intelligence alone. Complex non-linear interactions between:
1. Low attendance (< 75% university regulation threshold)
2. Cumulative standing backlogs
3. Low self-study allocation (< 2.5 hours/day)
4. Specific weaknesses in core technical subjects (Mathematics, DSA, DBMS, OS, CN, DMW)

result in unexpected semester failures. Faculty mentors lack real-time predictive tools to identify students in need of academic support before final examinations take place.

---

### **4. OBJECTIVES**
1. **Automated Data Wrangling:** Ingest, inspect, clean, and encode the 300-student cohort dataset while strictly preventing target leakage.
2. **Exploratory Data Analysis (EDA):** Uncover statistical correlations between attendance, backlogs, study hours, internal marks, and final performance.
3. **Comparative Machine Learning:** Train and benchmark Linear Regression, Decision Tree Regressor, and Random Forest Regressor under identical cross-validation conditions (80% train / 20% test).
4. **Early Academic Warning System:** Design rules to stratify students into Low Risk, Medium Risk, and High Risk categories.
5. **Interactive Decision Dashboard:** Deploy an intuitive Streamlit interface allowing mentors to search student profiles, filter cohorts, and predict student performance in real time.

---

### **5. LITERATURE REVIEW**
- **Cortez & Silva (2008):** In *"Using Data Mining to Predict Secondary School Student Performance"*, Cortez and Silva demonstrated that continuous formative assessments and past failures are the primary indicators of end-semester performance.
- **Romero & Ventura (2010):** Surveyed Educational Data Mining (EDM) applications, showing that supervised regression techniques accurately forecast student course outcomes when behavioral indicators like attendance and study hours are incorporated.
- **Baker et al. (2012):** Highlighted the critical importance of transparent, actionable decision-support dashboards for university mentors and counselors to avoid post-hoc academic failures.

---

### **6. EXISTING SYSTEM**
- Relies on manual gradebook spreadsheets or post-semester results declarations.
- Identifies failing students only after final grades are published.
- Ignores multi-variable interactions (e.g., how backlogs compound the effect of low attendance).

---

### **7. PROPOSED SYSTEM**
- Automated machine learning system integrating data wrangling, feature engineering, and continuous score prediction.
- Scikit-Learn `ColumnTransformer` guarantees zero target leakage.
- Automated Early Warning stratification:
  * **Excellent (85–100):** Eligible for advanced research projects and honors tracks.
  * **Very Good (70–84):** Solid academic trajectory.
  * **Good (60–69):** Satisfactory performance.
  * **Average (50–59):** Moderate risk; peer tutoring recommended.
  * **Needs Improvement (< 50):** High academic risk; mandatory remedial coaching.

---

### **8. SYSTEM REQUIREMENTS**
- **Operating System:** Windows 10/11, Linux, or macOS
- **Programming Language:** Python 3.10+
- **Libraries:** Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn, Plotly, Streamlit, Joblib
- **Hardware:** Intel Core i3 / AMD Ryzen 3 or higher, 4 GB RAM minimum

---

### **9. METHODOLOGY (CRISP-DM)**
The system adheres to the Cross-Industry Standard Process for Data Mining:
1. **Academic Understanding:** Define target score (0–100) and risk thresholds.
2. **Data Understanding:** Ingest cohort dataset, verify attribute types and distributions.
3. **Data Preparation:** Clean data, scale continuous features with `StandardScaler`, encode categorical attributes with `OneHotEncoder`.
4. **Modeling:** Benchmark Linear Regression, Decision Tree, and Random Forest.
5. **Evaluation:** Evaluate MAE, MSE, RMSE, and $R^2$ on 20% test data.
6. **Deployment:** Deploy Streamlit web dashboard with interactive Plotly visual analytics.

---

### **10. DATA WRANGLING TECHNIQUES**
1. **Missing Value Auditing:** 0 null values detected across all 300 student records.
2. **Duplicate Detection:** 0 duplicate Student IDs found.
3. **Range Constraints:** Enforced bounds on CGPA (0–10), Attendance (0–100%), and Subject Marks (0–100).
4. **Outlier Detection:** Used Interquartile Range (IQR) on `Absence_Days` ($Q_3 + 1.5 \times \text{IQR} = 24.5$ days), identifying 2 chronic absence cases.
5. **Standardization:** Zero-mean, unit-variance scaling on all numerical features.
6. **Categorical Encoding:** `OneHotEncoder(drop='first')` for Section, Gender, and Standing categories.

---

### **11. CORE ACADEMIC SUBJECTS (5TH SEMESTER)**
1. Advanced Engineering Mathematics
2. Data Structures and Algorithms
3. Database Management Systems
4. Operating Systems
5. Computer Networks
6. Data Mining and Data Wrangling

---

### **12. EXPERIMENTAL RESULTS AND DISCUSSION**

#### Evaluation on 20% Unseen Test Partition ($N=60$, `random_state=42`):

| Algorithm | Mean Absolute Error (MAE) | Mean Squared Error (MSE) | Root Mean Squared Error (RMSE) | $R^2$ Score (Variance Explained) |
| :--- | :---: | :---: | :---: | :---: |
| **Linear Regression** | **2.6087** | **11.3731** | **3.3724** | **0.9277 (92.8%)** 🏆 |
| **Random Forest Regressor** | 3.0100 | 15.1239 | 3.8889 | 0.9039 (90.4%) |
| **Decision Tree Regressor** | 4.4868 | 32.7749 | 5.7249 | 0.7918 (79.2%) |

#### Key Empirical Findings:
- Formative subject marks and previous CGPA are the strongest positive predictors of final semester performance.
- Backlog count and chronic absenteeism are the primary negative risk drivers.
- Linear Regression achieved the lowest RMSE ($3.37$) due to strong additive relationships across formative assessments.

---

### **13. EARLY WARNING PROTOCOLS**
- **High Risk:** Score $< 50$, Attendance $< 65\%$, or $\ge 3$ Backlogs $\rightarrow$ Mandatory remedial classes and parent-mentor alignment.
- **Medium Risk:** Score $50 - 59$, Attendance $65 - 74\%$, or $2$ Backlogs $\rightarrow$ Faculty mentor counseling and assignment recovery.
- **Low Risk:** Score $\ge 60$, Attendance $\ge 75\%$, $\le 1$ Backlogs $\rightarrow$ Standard tracking and project mentoring.

---

### **14. CONCLUSION**
EduPredict AI transforms academic monitoring at Sapthagiri NPS University from a reactive post-exam audit into an active early-warning system. With an $R^2$ score of $92.77\%$, the system provides mentors with reliable predictions and actionable guidance to help students succeed.
