# PRESENTATION & VIVA PREPARATION GUIDE

## Project: **EduPredict AI: Student Academic Performance Analysis and Prediction System**
### Institution: **Sapthagiri NPS University, Bengaluru, Karnataka, India**
### Department: **Department of Computer Science and Engineering**
### Academic Year: **2026–2027 | 5th Semester B.E.**
### Subject: **Data Mining and Data Wrangling (DMW)**

---

## 🎯 1. 2-MINUTE ELEVATOR PITCH TO YOUR EXAMINER

> *"Good morning/afternoon, Sir/Madam.*
>
> *My project is titled **'EduPredict AI: Student Academic Performance Analysis and Prediction System'**, developed for **Sapthagiri NPS University, Bengaluru**, Department of Computer Science and Engineering.*
>
> *Traditional academic evaluations evaluate students only after end-semester examinations conclude, when it is too late for remedial intervention.*
>
> *Our project establishes an **Early Academic Warning System** that analyzes a 5th-semester student's continuous internal assessment marks across six core subjects—Mathematics, DSA, DBMS, Operating Systems, Computer Networks, and Data Mining & Wrangling—alongside their previous CGPA, attendance percentage, daily study hours, and active backlog history.*
>
> *We implemented a data wrangling pipeline that audits missing values, inspects outliers using the Interquartile Range (IQR), and eliminates target leakage by fitting Scalers and Encoders strictly on the 80% training partition.*
>
> *We benchmarked three machine learning algorithms: **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor**. **Linear Regression** achieved the best generalization with an **$R^2$ score of 92.77%** and an **RMSE of 3.37 marks**.*
>
> *Finally, we deployed an interactive **Streamlit web application with Plotly visual analytics**, featuring an Executive Dashboard, Dataset Explorer, Early Warning System, and Individual Student 360-degree profiles."*

---

## 💡 2. CORE CONCEPTS: DATA MINING VS DATA WRANGLING

### **Q1: What is Data Wrangling?**
- **Definition:** Data Wrangling is the process of converting raw, messy, or unstructured data into a clean, structured, and validated format suitable for analysis and modeling.
- **In our project:**
  1. Verified 0 null values and 0 duplicate Student IDs across all 300 student records.
  2. Enforced value ranges (CGPA $\in [0, 10]$, Attendance $\in [0, 100\%]$, Subject Marks $\in [0, 100]$).
  3. Flagged absence outliers exceeding the IQR threshold ($Q_3 + 1.5 \times \text{IQR} = 24.5$ days).
  4. Standardized numerical metrics with `StandardScaler` and encoded nominal features with `OneHotEncoder(drop='first')`.

### **Q2: What is Data Mining?**
- **Definition:** Data Mining is the computational process of discovering non-trivial, hidden patterns, predictive models, and behavioral trends from datasets.
- **In our project:**
  1. Extracted multi-attribute correlation patterns (e.g., how backlogs and attendance interact with internal marks).
  2. Benchmarked supervised regression models.
  3. Identified top feature importances to determine the key drivers of engineering student success.

---

## 🤖 3. EXPLANATION OF MACHINE LEARNING ALGORITHMS

### **1. Linear Regression (🏆 Best Model)**
- **How it works:** Models the relationship between the target score and input features by minimizing the Sum of Squared Residuals (Ordinary Least Squares):
  $$\hat{y} = \beta_0 + \sum_{i=1}^p \beta_i x_i$$
- **Pros:** Highly interpretable coefficients, lowest variance, no hyperparameter tuning complexity.
- **Result:** **$R^2 = 0.9277$**, **$\text{RMSE} = 3.3724$**, **$\text{MAE} = 2.6087$**.
- **Why it won:** Formative internal marks and previous CGPA have a strong additive linear relationship with the final aggregate score.

### **2. Random Forest Regressor**
- **How it works:** An ensemble bagging method that builds 120 decorrelated decision trees, each trained on random bootstrap samples of students and features, averaging their predictions.
- **Result:** $R^2 = 0.9039$, $\text{RMSE} = 3.8889$, $\text{MAE} = 3.0100$.

### **3. Decision Tree Regressor**
- **How it works:** Recursively partitions the feature space using binary decision thresholds that maximize variance reduction (MSE minimization).
- **Result:** $R^2 = 0.7918$, $\text{RMSE} = 5.7249$, $\text{MAE} = 4.4868$.

---

## ❓ 4. TOP 10 FREQUENTLY ASKED VIVA QUESTIONS & MODEL ANSWERS

### **Q1: What are the 6 core 5th-semester subjects in your project?**
> *"1. Advanced Engineering Mathematics*
> *2. Data Structures and Algorithms*
> *3. Database Management Systems*
> *4. Operating Systems*
> *5. Computer Networks*
> *6. Data Mining and Data Wrangling"*

### **Q2: What is Target Leakage and how did you prevent it?**
> *"Target leakage occurs when information from outside the training dataset (or future information) is inadvertently used to train the model. We prevented this by wrapping our `ColumnTransformer` (StandardScaler + OneHotEncoder) inside a Scikit-Learn `Pipeline` that was fitted **strictly on the 80% training set** ($N=240$), preventing test data statistics from leaking into the training phase."*

### **Q3: What evaluation metrics did you use and why?**
> *"1. **MAE (Mean Absolute Error):** Measures average absolute error in marks ($2.61$ marks for Linear Regression).*
> *2. **RMSE (Root Mean Squared Error):** Penalizes larger prediction errors heavily ($3.37$ marks).*
> *3. **$R^2$ Score (Coefficient of Determination):** Explains the percentage of variance captured ($92.77\%$)."*

### **Q4: How does your Early Academic Warning System categorize students?**
> *"We use three transparent tiers:*
> *• **High Risk:** Predicted score $< 50$, attendance $< 65\%$, or $\ge 3$ backlogs $\rightarrow$ Triggers mandatory remedial classes and parent-mentor meetings.*
> *• **Medium Risk:** Predicted score $50 - 59$, attendance $65 - 74\%$, or $2$ backlogs $\rightarrow$ Faculty counseling and assignment recovery.*
> *• **Low Risk:** Predicted score $\ge 60$, attendance $\ge 75\%$, $\le 1$ backlog $\rightarrow$ Standard tracking."*

### **Q5: Why is attendance a critical feature in the model?**
> *"University regulations mandate at least 75% attendance for examination eligibility. In our correlation analysis, attendance showed an $r \approx 0.62$ positive correlation with marks, while students below 65% exhibited a steep drop in CIE scores."*

---

## 📊 5. 10-SLIDE PRESENTATION OUTLINE

- **Slide 1:** Title Slide (EduPredict AI, Sapthagiri NPS University, Dept. of CSE, Name, Roll No.)
- **Slide 2:** Motivation & Problem Statement (Reactive grading vs Proactive Early Warning)
- **Slide 3:** Project Objectives & University Curriculum Integration (6 Core 5th-Sem Subjects)
- **Slide 4:** Dataset Schema & Data Wrangling Diagnostics (Auditing, IQR Outlier Detection)
- **Slide 5:** Exploratory Data Analysis (Correlation Heatmap, Attendance vs Marks, Subject Variance)
- **Slide 6:** Machine Learning Architecture & Anti-Leakage Preprocessing Pipeline
- **Slide 7:** Model Benchmarking & Performance Comparison (LR vs DT vs RF)
- **Slide 8:** Early Academic Warning System & Intervention Protocols
- **Slide 9:** Live Streamlit Web Dashboard Demonstration (`http://localhost:8501`)
- **Slide 10:** Conclusion, Project Impact, and Future Enhancements
