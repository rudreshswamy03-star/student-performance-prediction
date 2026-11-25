"""
Interactive Web Application: Student Performance Prediction Using Data Mining
Course: Data Mining and Data Wrangling
Framework: Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import os

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="EduPredict | Student Performance Prediction",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for a polished academic dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .badge-excellent {
        background-color: #DCFCE7;
        color: #166534;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
    }
    .badge-good {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
    }
    .badge-pass {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
    }
    .badge-risk {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 1.1rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# CACHED DATA & MODEL LOADERS
# ---------------------------------------------------------
@st.cache_data
def load_data():
    filepath = os.path.join("dataset", "student-mat.csv")
    df = pd.read_csv(filepath, sep=';')
    return df

@st.cache_resource
def load_model():
    model_path = os.path.join("model", "best_model.joblib")
    return joblib.load(model_path)

@st.cache_data
def load_metrics():
    metrics_path = os.path.join("model", "model_metrics.json")
    with open(metrics_path, "r") as f:
        return json.load(f)

# Load resources
try:
    df_raw = load_data()
    pipeline = load_model()
    metrics_data = load_metrics()
except Exception as e:
    st.error(f"Error loading project artifacts: {e}. Please ensure data and models are prepared.")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎓 EduPredict AI")
    st.markdown("**Data Mining & Wrangling Project**")
    st.markdown("---")
    
    st.markdown("### 📌 Navigation")
    selected_tab = st.radio(
        "Go to Module:",
        ["📋 Overview & Dataset", "📈 Exploratory Data Analysis", "🤖 Model Evaluation", "🎯 Performance Predictor"],
        index=3
    )
    
    st.markdown("---")
    st.markdown("### 📊 Dataset Quick Stats")
    st.markdown(f"• **Total Students:** {df_raw.shape[0]}")
    st.markdown(f"• **Attributes:** {df_raw.shape[1]}")
    st.markdown(f"• **Target Metric:** `G3` (Final Grade: 0-20)")
    st.markdown(f"• **Average Final Grade:** {df_raw['G3'].mean():.2f} / 20")
    st.markdown("---")
    st.caption("Developed for Academic Evaluation & Early Warning System")

# ---------------------------------------------------------
# MODULE 1: PROJECT OVERVIEW & DATASET
# ---------------------------------------------------------
if selected_tab == "📋 Overview & Dataset":
    st.markdown("<div class='main-header'>Student Performance Prediction Using Data Mining</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Academic Project Overview, Dataset Inspection, and Preprocessing Diagnostics</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{df_raw.shape[0]} students")
    with col2:
        st.metric("Input Features", f"{df_raw.shape[1] - 1}")
    with col3:
        st.metric("Missing Values", f"{df_raw.isnull().sum().sum()} (0.0%)")
    with col4:
        st.metric("Target Variable", "G3 (0 - 20)")
        
    st.markdown("### 🎯 Project Objectives")
    st.markdown("""
    1. **Early Academic Intervention:** Identify students at risk of underperforming before the final examination.
    2. **Pattern Discovery:** Reveal how study hours, absences, prior examination marks, and social variables affect learning outcomes.
    3. **Rigorous Machine Learning Comparison:** Benchmark **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor** using unified cross-validated pipelines to avoid data leakage.
    4. **Actionable Decision Support:** Provide an intuitive web tool for educators and counselors.
    """)
    
    st.markdown("### 🔍 Dataset Explorer (UCI Machine Learning Repository)")
    filter_school = st.multiselect("Filter by School:", options=df_raw['school'].unique(), default=df_raw['school'].unique())
    filter_sex = st.multiselect("Filter by Sex:", options=df_raw['sex'].unique(), default=df_raw['sex'].unique())
    
    filtered_df = df_raw[(df_raw['school'].isin(filter_school)) & (df_raw['sex'].isin(filter_sex))]
    st.dataframe(filtered_df.head(50), use_container_width=True)
    
    with st.expander("📖 View Complete Attribute Definitions & Descriptions"):
        st.markdown("""
        * **school:** Student's school ('GP' - Gabriel Pereira, 'MS' - Mousinho da Silveira)
        * **sex:** Student's sex ('F' - female, 'M' - male)
        * **age:** Student's age (15 to 22)
        * **studytime:** Weekly study time (1: <2 hrs, 2: 2-5 hrs, 3: 5-10 hrs, 4: >10 hrs)
        * **failures:** Number of past class failures (0 to 3)
        * **absences:** Number of school absences (0 to 93)
        * **G1:** First period grade (0 to 20)
        * **G2:** Second period grade (0 to 20)
        * **G3:** Final examination grade (0 to 20) - **Target Variable**
        """)

# ---------------------------------------------------------
# MODULE 2: EXPLORATORY DATA ANALYSIS (EDA)
# ---------------------------------------------------------
elif selected_tab == "📈 Exploratory Data Analysis":
    st.markdown("<div class='main-header'>Exploratory Data Analysis (EDA)</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Discovering Academic Trends, Feature Relationships, and Correlations</div>", unsafe_allow_html=True)
    
    row1_c1, row1_c2 = st.columns(2)
    
    with row1_c1:
        st.subheader("1. Final Grade (G3) Distribution")
        fig, ax = plt.subplots(figsize=(7, 4.2))
        sns.histplot(df_raw['G3'], bins=20, kde=True, color="#2563EB", ax=ax)
        ax.set_title("Distribution of Final Marks (G3)", fontsize=13, fontweight='bold')
        ax.set_xlabel("Final Grade (0 to 20)")
        ax.set_ylabel("Student Count")
        ax.axvline(10, color='red', linestyle='--', label='Passing Mark (10/20)')
        ax.legend()
        st.pyplot(fig)
        st.caption("💡 **Insight:** Grades are normally distributed around the mean of 10.4, with a distinct spike at 0 representing students who missed the exam or dropped out.")

    with row1_c2:
        st.subheader("2. Weekly Study Time vs Final Grade")
        fig, ax = plt.subplots(figsize=(7, 4.2))
        study_labels = {1: "< 2 hrs", 2: "2-5 hrs", 3: "5-10 hrs", 4: "> 10 hrs"}
        plot_df = df_raw.copy()
        plot_df['study_label'] = plot_df['studytime'].map(study_labels)
        sns.boxplot(x='study_label', y='G3', data=plot_df, palette="Blues", ax=ax, order=["< 2 hrs", "2-5 hrs", "5-10 hrs", "> 10 hrs"])
        ax.set_title("Final Marks Across Study Time Intervals", fontsize=13, fontweight='bold')
        ax.set_xlabel("Weekly Study Hours")
        ax.set_ylabel("Final Grade (G3)")
        st.pyplot(fig)
        st.caption("💡 **Insight:** Median final marks rise consistently as weekly study time increases from under 2 hours to above 10 hours.")

    row2_c1, row2_c2 = st.columns(2)
    
    with row2_c1:
        st.subheader("3. Absences vs Final Grade (Scatter)")
        fig, ax = plt.subplots(figsize=(7, 4.2))
        sns.regplot(x='absences', y='G3', data=df_raw, color="#DC2626", scatter_kws={'alpha': 0.6}, line_kws={'color': '#7F1D1D'}, ax=ax)
        ax.set_title("Student Absences vs Final Exam Marks", fontsize=13, fontweight='bold')
        ax.set_xlabel("Total Absences")
        ax.set_ylabel("Final Grade (G3)")
        st.pyplot(fig)
        st.caption("💡 **Insight:** Excessive absences display a negative association with academic success. Regular attendance is critical for exam retention.")

    with row2_c2:
        st.subheader("4. Second Period Mark (G2) vs Final Mark (G3)")
        fig, ax = plt.subplots(figsize=(7, 4.2))
        sns.scatterplot(x='G2', y='G3', hue='sex', data=df_raw, palette={'F': '#EC4899', 'M': '#3B82F6'}, alpha=0.8, s=60, ax=ax)
        sns.lineplot(x=[0, 20], y=[0, 20], color='gray', linestyle='--', ax=ax)
        ax.set_title("Internal Assessment (G2) vs Final Grade (G3)", fontsize=13, fontweight='bold')
        ax.set_xlabel("Period 2 Grade (G2)")
        ax.set_ylabel("Final Grade (G3)")
        st.pyplot(fig)
        st.caption("💡 **Insight:** Strong positive linear correlation ($r > 0.90$) confirms prior academic test performance is the strongest predictor of final performance.")

    st.subheader("5. Correlation Heatmap of Numerical Features")
    fig, ax = plt.subplots(figsize=(11, 6))
    num_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'G1', 'G2', 'G3']
    corr_matrix = df_raw[num_cols].corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax, annot_kws={"size": 8})
    ax.set_title("Attribute Pearson Correlation Matrix", fontsize=14, fontweight='bold')
    st.pyplot(fig)

# ---------------------------------------------------------
# MODULE 3: MODEL BENCHMARKING & EVALUATION
# ---------------------------------------------------------
elif selected_tab == "🤖 Model Evaluation":
    st.markdown("<div class='main-header'>Machine Learning Model Benchmark & Comparison</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Rigorous Evaluation on Unseen 20% Testing Set (Reproducible Random State = 42)</div>", unsafe_allow_html=True)
    
    results = metrics_data["metrics"]
    metrics_df = pd.DataFrame(results).T
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Best Model Selected", metrics_data["best_model_name"])
    with c2:
        st.metric("Lowest Test RMSE", f"{results[metrics_data['best_model_name']]['RMSE']}")
    with c3:
        st.metric("Highest Test R² Score", f"{results[metrics_data['best_model_name']]['R2']}")

    st.markdown("### 📊 Experimental Comparison Table")
    st.dataframe(metrics_df.style.highlight_min(subset=["MAE", "RMSE"], color="#DCFCE7").highlight_max(subset=["R2"], color="#DCFCE7"), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Model Performance by Metric")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        metrics_df[['MAE', 'RMSE']].plot(kind='bar', ax=ax, colormap="viridis")
        ax.set_title("MAE vs RMSE Comparison (Lower is Better)", fontweight='bold')
        ax.set_ylabel("Error Points (on 0-20 scale)")
        ax.set_xticklabels(metrics_df.index, rotation=0)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

    with col2:
        st.subheader("Variance Explained ($R^2$ Score)")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        metrics_df['R2'].plot(kind='bar', color='#3B82F6', ax=ax)
        ax.set_title("R-squared ($R^2$) Score (Higher is Better)", fontweight='bold')
        ax.set_ylabel("R² Coefficient")
        ax.set_ylim(0, 1.0)
        ax.set_xticklabels(metrics_df.index, rotation=0)
        for i, v in enumerate(metrics_df['R2']):
            ax.text(i, v + 0.02, f"{v:.4f}", ha='center', fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig)

    st.markdown("### 🌟 Feature Importance Analysis (Top Drivers)")
    feat_df = pd.DataFrame(metrics_data["feature_importances"])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.barplot(x="importance", y="feature", data=feat_df, palette="crest", ax=ax)
    ax.set_title(f"Top 15 Most Influential Features in {metrics_data['best_model_name']}", fontweight='bold')
    ax.set_xlabel("Relative Importance Weight")
    ax.set_ylabel("Feature Name")
    st.pyplot(fig)

# ---------------------------------------------------------
# MODULE 4: STUDENT PERFORMANCE PREDICTOR
# ---------------------------------------------------------
elif selected_tab == "🎯 Performance Predictor":
    st.markdown("<div class='main-header'>Student Performance Prediction Tool</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Input Academic and Behavioral Profile to Predict Final Exam Grade & Support Status</div>", unsafe_allow_html=True)

    with st.form("prediction_form"):
        st.markdown("#### 1. Academic Assessments & Prior Performance")
        c1, c2, c3 = st.columns(3)
        with c1:
            g1 = st.slider("First Period Grade (G1):", min_value=0, max_value=20, value=12, help="Internal Exam 1 score out of 20")
        with c2:
            g2 = st.slider("Second Period Grade (G2):", min_value=0, max_value=20, value=13, help="Internal Exam 2 score out of 20")
        with c3:
            failures = st.selectbox("Past Class Failures:", options=[0, 1, 2, 3], index=0, help="Number of past course failures")

        st.markdown("#### 2. Study Habits, Attendance & Academic Support")
        c4, c5, c6, c7 = st.columns(4)
        with c4:
            studytime = st.selectbox("Weekly Study Time:", options=[1, 2, 3, 4], 
                                     format_func=lambda x: {1: "< 2 hours", 2: "2 - 5 hours", 3: "5 - 10 hours", 4: "> 10 hours"}[x], index=1)
        with c5:
            absences = st.number_input("School Absences (Days):", min_value=0, max_value=93, value=4, step=1)
        with c6:
            schoolsup = st.selectbox("Extra Educational Support:", options=["yes", "no"], index=1)
        with c7:
            famsup = st.selectbox("Family Educational Support:", options=["yes", "no"], index=0)

        st.markdown("#### 3. Personal, Demographics & Family Background")
        c8, c9, c10, c11 = st.columns(4)
        with c8:
            age = st.slider("Age:", min_value=15, max_value=22, value=17)
        with c9:
            sex = st.selectbox("Sex:", options=["F", "M"], format_func=lambda x: "Female" if x=="F" else "Male")
        with c10:
            school = st.selectbox("School:", options=["GP", "MS"], format_func=lambda x: "Gabriel Pereira (GP)" if x=="GP" else "Mousinho da Silveira (MS)")
        with c11:
            address = st.selectbox("Address Location:", options=["U", "R"], format_func=lambda x: "Urban" if x=="U" else "Rural")

        c12, c13, c14, c15 = st.columns(4)
        with c12:
            medu = st.selectbox("Mother's Education:", options=[0, 1, 2, 3, 4], 
                                format_func=lambda x: {0: "None", 1: "Primary", 2: "5th-9th grade", 3: "Secondary", 4: "Higher education"}[x], index=3)
        with c13:
            fedu = st.selectbox("Father's Education:", options=[0, 1, 2, 3, 4], 
                                format_func=lambda x: {0: "None", 1: "Primary", 2: "5th-9th grade", 3: "Secondary", 4: "Higher education"}[x], index=2)
        with c14:
            mjob = st.selectbox("Mother's Occupation:", options=["teacher", "health", "services", "at_home", "other"], index=2)
        with c15:
            fjob = st.selectbox("Father's Occupation:", options=["teacher", "health", "services", "at_home", "other"], index=4)

        c16, c17, c18, c19 = st.columns(4)
        with c16:
            higher = st.selectbox("Aspires for Higher Education:", options=["yes", "no"], index=0)
        with c17:
            internet = st.selectbox("Internet Access at Home:", options=["yes", "no"], index=0)
        with c18:
            paid = st.selectbox("Extra Paid Classes in Math:", options=["yes", "no"], index=1)
        with c19:
            activities = st.selectbox("Extra-Curricular Activities:", options=["yes", "no"], index=0)

        st.markdown("#### 4. Social & Health Indicators")
        c20, c21, c22, c23 = st.columns(4)
        with c20:
            freetime = st.slider("Free Time After School (1-5):", min_value=1, max_value=5, value=3)
        with c21:
            goout = st.slider("Going Out with Friends (1-5):", min_value=1, max_value=5, value=2)
        with c22:
            walc = st.slider("Weekend Alcohol Consumption (1-5):", min_value=1, max_value=5, value=1)
        with c23:
            health = st.slider("Current Health Status (1-5):", min_value=1, max_value=5, value=4)

        # Hidden defaults for standard fixed demographic features to keep UI streamlined
        famsize = "GT3"
        pstatus = "T"
        reason = "course"
        guardian = "mother"
        traveltime = 1
        nursery = "yes"
        romantic = "no"
        famrel = 4
        dalc = 1

        submit_btn = st.form_submit_button("🔮 Predict Final Examination Performance", use_container_width=True)

    if submit_btn:
        student_input = {
            'school': school, 'sex': sex, 'age': age, 'address': address, 'famsize': famsize, 'Pstatus': pstatus,
            'Medu': medu, 'Fedu': fedu, 'Mjob': mjob, 'Fjob': fjob, 'reason': reason, 'guardian': guardian,
            'traveltime': traveltime, 'studytime': studytime, 'failures': failures, 'schoolsup': schoolsup,
            'famsup': famsup, 'paid': paid, 'activities': activities, 'nursery': nursery, 'higher': higher,
            'internet': internet, 'romantic': romantic, 'famrel': famrel, 'freetime': freetime, 'goout': goout,
            'Dalc': dalc, 'Walc': walc, 'health': health, 'absences': absences, 'G1': g1, 'G2': g2
        }
        
        # Inference using trained pipeline
        input_df = pd.DataFrame([student_input])
        raw_pred = float(pipeline.predict(input_df)[0])
        predicted_grade = round(max(0.0, min(20.0, raw_pred)), 2)
        percentage = round((predicted_grade / 20.0) * 100, 1)

        st.markdown("---")
        st.subheader("🎓 Prediction Results & Academic Advisory")

        res_c1, res_c2, res_c3 = st.columns([1, 1, 2])
        
        with res_c1:
            st.metric("Predicted Final Grade (G3)", f"{predicted_grade} / 20")
        with res_c2:
            st.metric("Equivalent Percentage", f"{percentage}%")
            
        with res_c3:
            if predicted_grade >= 16:
                st.markdown("<div class='badge-excellent'>🌟 Distinction / Top Tier</div>", unsafe_allow_html=True)
                st.markdown("**Advisory:** Student displays exceptional academic trajectory. Recommended for advanced projects and peer mentoring.")
            elif predicted_grade >= 14:
                st.markdown("<div class='badge-good'>✅ Good Academic Standing</div>", unsafe_allow_html=True)
                st.markdown("**Advisory:** Solid performance. Maintain consistent study hours and test preparation to sustain this standing.")
            elif predicted_grade >= 10:
                st.markdown("<div class='badge-pass'>⚠️ Pass / Needs Monitoring</div>", unsafe_allow_html=True)
                st.markdown("**Advisory:** Student is passing but near borderline. Weekly problem-solving sessions and absence checks recommended.")
            else:
                st.markdown("<div class='badge-risk'>🚨 HIGH RISK: Academic Failure Likely</div>", unsafe_allow_html=True)
                st.markdown("**Early Warning Intervention:** Student requires immediate remedial classes, counseling, and parent-teacher alignment!")

        # Visual progress bar for percentage
        st.markdown("#### Academic Performance Meter")
        st.progress(percentage / 100.0)
