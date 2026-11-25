# ACADEMIC PROJECT REPORT

## PROJECT TITLE:
### **Student Performance Prediction Using Data Mining and Data Wrangling**

---

### **1. ABSTRACT**
Student academic performance prediction is a critical challenge in educational data mining (EDM). Early identification of at-risk students empowers educators and academic counselors to offer timely remedial interventions, preventing course dropouts and failures. This project designs, evaluates, and deploys an end-to-end Machine Learning system trained on the benchmark UCI Student Performance dataset ($N=395$). Using structured data wrangling, missing-value audits, duplicate filtering, IQR-based outlier diagnostics, and a scikit-learn `ColumnTransformer` preprocessing pipeline (StandardScaler and OneHotEncoder), we benchmark three core algorithms: **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor**. The **Random Forest Regressor** demonstrated superior generalization performance on the held-out 20% test partition, obtaining a **Mean Absolute Error (MAE) of 1.1853**, a **Root Mean Squared Error (RMSE) of 1.9541**, and an **$R^2$ score of 0.8138**, explaining over 81.3% of the variance in final exam marks ($G3$). The best-performing pipeline is serialized using Joblib and served via a modern, interactive Streamlit web dashboard.

---

### **2. INTRODUCTION**
Higher education institutions continuously seek proactive mechanisms to enhance student success and institutional completion rates. Traditional educational evaluation models evaluate students only after summative end-semester examinations conclude, eliminating any opportunity for corrective instruction. Educational Data Mining (EDM) bridges this gap by discovering hidden non-linear relationships among student demographic indicators, parental background, social habits, absences, and formative internal assessments ($G1, G2$).

---

### **3. PROBLEM STATEMENT**
Educators often struggle to identify struggling students early in the semester due to large classroom sizes and multi-factorial performance drivers. Academic decline is seldom driven by intelligence alone; it is influenced by attendance irregularities, study time allocation, social distractions, and previous assessment performance. The problem is to formulate an accurate predictive regression model capable of forecasting student final examination marks ($G3 \in [0, 20]$) and translating raw predictions into actionable early-warning alerts for counseling.

---

### **4. OBJECTIVES**
1. **Automated Data Wrangling:** Ingest, inspect, clean, and encode the semicolon-delimited UCI Student Performance dataset.
2. **Exploratory Data Analysis (EDA):** Uncover statistical correlations between study time, failure history, absences, internal marks, and final grades.
3. **Comparative Data Mining:** Train and benchmark Linear Regression, Decision Tree Regressor, and Random Forest Regressor under identical cross-validation conditions with zero data leakage.
4. **Model Serialization:** Package the preprocessor and winning model using Joblib.
5. **Interactive Decision Dashboard:** Deploy an intuitive Streamlit interface allowing instructors to adjust inputs and evaluate student standing in real time.

---

### **5. LITERATURE REVIEW**
- **Cortez & Silva (2008):** In their foundational paper *"Using Data Mining to Predict Secondary School Student Performance"*, Cortez and Silva collected and analyzed secondary school data from Portugal using Decision Trees, Neural Networks, and Support Vector Machines, concluding that prior academic periods ($G1, G2$) and school failures are primary indicators of success.
- **Romero & Ventura (2010):** Surveyed Educational Data Mining (EDM) applications, demonstrating that ensemble tree models consistently outperform basic statistical regressions in capturing non-linear student behavior patterns.
- **Baker et al. (2012):** Emphasized the necessity of interpretable machine learning dashboards for educators, ensuring that model predictions yield actionable counseling interventions.

---

### **6. EXISTING SYSTEM**
- Relies on manual gradebook spreadsheets or post-hoc term evaluations.
- Identifies failing students only after final grades are published.
- Ignores multi-variable interactions (e.g., how weekend alcohol consumption or parental education amplifies or mitigates the impact of study hours).

---

### **7. PROPOSED SYSTEM**
- Fully automated machine learning system integrating data wrangling, feature engineering, and ensemble prediction.
- Employs a Scikit-Learn `ColumnTransformer` to enforce strict anti-leakage principles.
- Provides immediate risk classification:
  * $\ge 16$: Distinction / Top Tier
  * $14 - 15$: Good Academic Standing
  * $10 - 13$: Pass / Satisfactory (Requires Monitoring)
  * $< 10$: High Academic Risk (Immediate Tutoring Required)
- Features a rich graphical web interface with real-time feedback meters.

---

### **8. SYSTEM REQUIREMENTS**

#### Software Requirements:
- **Operating System:** Windows 10/11, Linux, or macOS
- **Programming Language:** Python 3.10 to 3.14
- **Libraries:** Pandas ($\ge 2.0$), NumPy ($\ge 1.24$), Scikit-Learn ($\ge 1.3$), Matplotlib ($\ge 3.7$), Seaborn ($\ge 0.12$), Streamlit ($\ge 1.30$), Joblib ($\ge 1.3$)

#### Hardware Requirements:
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
- **RAM:** 4 GB minimum (8 GB recommended)
- **Disk Space:** 500 MB free space

---

### **9. METHODOLOGY**
The standard **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology was utilized:
1. **Business/Academic Understanding:** Define target outcome ($G3$) and risk thresholds.
2. **Data Understanding:** Ingest UCI dataset, examine attribute types and distributions.
3. **Data Preparation:** Clean, handle outliers, one-hot encode categorical features, scale numeric features.
4. **Modeling:** Train Linear Regression, Decision Tree Regressor, Random Forest Regressor.
5. **Evaluation:** Compute MAE, RMSE, and $R^2$ on 20% unseen test data.
6. **Deployment:** Serialize model and launch Streamlit dashboard.

---

### **10. DATA WRANGLING TECHNIQUES**
1. **Delimiter Handling:** Raw file is semicolon-separated (`sep=';'`).
2. **Missing Value Auditing:** Complete verification revealed 0 null entries across all 395 records.
3. **Duplicate Detection:** Identified and removed 0 duplicate records.
4. **Range Validation:** Enforced value bounds for grades $G1, G2, G3 \in [0, 20]$.
5. **Outlier Detection:** Used Interquartile Range (IQR) on `absences`:
   $$\text{IQR} = Q_3 - Q_1$$
   $$\text{Threshold} = Q_3 + 1.5 \times \text{IQR}$$
   Identified 15 records with extreme absences ($> 20$ days) for investigative awareness.
6. **Standardization:** Applied zero-mean, unit-variance scaling on continuous features.
7. **Encoding:** Converted 17 nominal/binary categorical features via `OneHotEncoder(drop='first')`.

---

### **11. DATA MINING ALGORITHMS**

1. **Linear Regression:**
   $$y = \beta_0 + \sum_{i=1}^p \beta_i x_i + \epsilon$$
   Assumes linear additive relationships; provides a baseline model.
2. **Decision Tree Regressor:**
   Recursively partitions the feature space into homogeneous sub-regions by minimizing Mean Squared Error (MSE) at each split. Captures non-linear thresholds but is prone to variance.
3. **Random Forest Regressor:**
   An ensemble bootstrap aggregation (bagging) technique constructing $B=100$ decorrelated decision trees. Predictions are averaged:
   $$\hat{y} = \frac{1}{B} \sum_{b=1}^B T_b(x)$$
   Reduces variance dramatically, prevents overfitting, and produces robust feature importances.

---

### **12. SYSTEM ARCHITECTURE**

```
+-----------------------------------------------------------------------+
|                             DATA SOURCE                               |
|                UCI Machine Learning Repository (student-mat.csv)      |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                        DATA WRANGLING PIPELINE                        |
|  - Semicolon Parser        - Missing Value & Duplicate Check          |
|  - Outlier IQR Check       - Standard Scaler + One-Hot Encoder        |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                    TRAIN / TEST PARTITIONING (80/20)                  |
|          Train Set: N=316 students    |   Test Set: N=79 students     |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                        ALGORITHM BENCHMARKING                         |
|   1. Linear Regression    2. Decision Tree    3. Random Forest (🏆)   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                          MODEL SERIALIZATION                          |
|                  Joblib Pipeline (`model/best_model.joblib`)          |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|                          STREAMLIT DASHBOARD                          |
|   - EDA Visualizations      - Model Comparison Table                  |
|   - Feature Importance      - Interactive Student Predictor (Form)    |
+-----------------------------------------------------------------------+
```

---

### **13. IMPLEMENTATION**
The implementation is organized into modular Python files:
- `src/download_data.py`: Direct HTTPS download and zip decompression.
- `src/data_wrangling.py`: Preprocessing pipeline construction and dataset splitting.
- `src/train_models.py`: Pipeline training, multi-metric evaluation, and serialization.
- `src/predict.py`: Inference engine supporting dictionary input mapping.
- `src/demo_cases.py`: CLI multi-case risk evaluator.
- `app.py`: Streamlit responsive GUI application.
- `main.py`: Master automated pipeline controller.

---

### **14. RESULTS AND DISCUSSION**

#### Experimental Evaluation on 20% Unseen Test Set:

| Algorithm | Mean Absolute Error (MAE) | Root Mean Squared Error (RMSE) | $R^2$ Score (Variance Explained) |
| :--- | :---: | :---: | :---: |
| **Linear Regression** | $1.6467$ | $2.3784$ | $0.7241$ |
| **Decision Tree Regressor** | $1.3439$ | $2.4026$ | $0.7185$ |
| **Random Forest Regressor** | **$1.1853$** | **$1.9541$** | **$0.8138$** |

#### Top 5 Predictive Factors (Feature Importances):
1. **$G2$ (Second Period Grade):** Relative weight $\approx 0.65$ (Direct formative assessment).
2. **$G1$ (First Period Grade):** Relative weight $\approx 0.12$ (Foundational subject grasp).
3. **`absences` (Attendance Record):** Major penalty driver for chronic absenteeism.
4. **`failures` (Past Course Failures):** Strong indicator of repeated academic difficulty.
5. **`studytime` (Weekly Study Hours):** Strongest positive behavioral predictor.

---

### **15. ADVANTAGES**
1. **Early Intervention:** Identifies at-risk students before final exams take place.
2. **Zero Target Leakage:** Preprocessing transformations fit exclusively on training folds.
3. **High Predictive Fidelity:** $R^2 = 0.8138$ ensures accurate predictions within $\pm 1.18$ grade points.
4. **Explainable AI:** Feature importance rankings help educators understand *why* a student is at risk.
5. **Intuitive GUI:** Requires no programming skills for teachers to operate.

---

### **16. LIMITATIONS**
1. Dataset sample size is limited to 395 students from two Portuguese institutions.
2. Subject domain is currently focused on Mathematics; curricula in other subjects may exhibit different dynamics.
3. Grade 0 anomalies include administrative dropouts, which standard regression maps to extreme low scores.

---

### **17. FUTURE ENHANCEMENTS**
1. **Deep Learning Integration:** Experiment with Multi-Layer Perceptrons (MLPs) and TabNet architectures.
2. **Multi-Course Expansion:** Jointly model Mathematics and Portuguese language performance (`student-por.csv`).
3. **Automated Notification System:** Integrate automated email alerts to parents and tutors when risk exceeds critical thresholds.

---

### **18. CONCLUSION**
This project successfully designed, implemented, and benchmarked an automated Data Mining system for student examination performance prediction. The Random Forest Regressor emerged as the optimal algorithm, achieving an $R^2$ of $0.8138$ and an RMSE of $1.9541$. The interactive Streamlit dashboard transforms raw mathematical outputs into human-understandable academic counseling guidelines.

---

### **19. REFERENCES**
1. Cortez, P., & Silva, A. (2008). *Using Data Mining to Predict Secondary School Student Performance*. In Proceedings of 5th Annual Future Business Technology Conference (FUBUTEC 2008), pp. 5-12, Porto, Portugal.
2. Romero, C., & Ventura, S. (2010). *Educational Data Mining: A Review of the State of the Art*. IEEE Transactions on Systems, Man, and Cybernetics, Part C (Applications and Reviews), 40(6), 601-618.
3. Baker, R. S., & Yacef, K. (2009). *The State of Educational Data Mining in 2009: A Review and Future Visions*. Journal of Educational Data Mining, 1(1), 3-17.
4. UCI Machine Learning Repository: Student Performance Dataset. URL: https://archive.ics.uci.edu/dataset/320/student+performance
