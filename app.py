"""
================================================================================
EduPredict AI: Student Academic Performance Analysis and Prediction System
Institution : Sapthagiri NPS University, Bengaluru, Karnataka, India
Department  : Department of Computer Science and Engineering
Academic Yr : 2026–2027 | Undergraduate Engineering (5th Semester)
Subject     : Data Mining and Data Wrangling Capstone
Framework   : Streamlit with Interactive Plotly Visualizations
================================================================================
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EduPredict AI | Sapthagiri NPS University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS: CLEAN UNIVERSITY THEME (NAVY BLUE, SUBTLE PURPLE, CRISP CARDS)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Global Container */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    
    /* Headers & Branding */
    .univ-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 65%, #312E81 100%);
        color: #FFFFFF;
        padding: 22px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.12);
    }
    .univ-title {
        font-size: 1.65rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0;
        color: #FFFFFF;
    }
    .univ-subtitle {
        font-size: 0.95rem;
        color: #CBD5E1;
        margin-top: 4px;
        font-weight: 400;
    }
    .univ-meta {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 10px;
        color: #E2E8F0;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.08);
        border-color: #CBD5E1;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 4px 0;
    }
    .kpi-label {
        font-size: 0.82rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #94A3B8;
    }

    /* Status Badges */
    .badge-excellent {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-verygood {
        background-color: #EFF6FF;
        color: #1E40AF;
        border: 1px solid #BFDBFE;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-good {
        background-color: #F5F3FF;
        color: #5B21B6;
        border: 1px solid #DDD6FE;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-average {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
    }
    .badge-risk {
        background-color: #FEF2F2;
        color: #991B1B;
        border: 1px solid #FECACA;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.95rem;
        display: inline-block;
    }

    /* Section Subheading Card */
    .section-head {
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 8px;
        margin: 20px 0 16px 0;
        font-weight: 700;
        color: #0F172A;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# RESOURCE CACHING & LOADERS
# -----------------------------------------------------------------------------
@st.cache_data
def load_cohort_data():
    csv_path = os.path.join("dataset", "university_students.csv")
    if not os.path.exists(csv_path):
        from generate_university_data import save_university_dataset
        save_university_dataset(csv_path)
    return pd.read_csv(csv_path)

@st.cache_resource
def load_model_pipeline():
    model_path = os.path.join("model", "best_model.joblib")
    if not os.path.exists(model_path):
        from train_models import train_and_evaluate_models
        train_and_evaluate_models()
    return joblib.load(model_path)

@st.cache_data
def load_model_metadata():
    json_path = os.path.join("model", "model_metrics.json")
    if not os.path.exists(json_path):
        from train_models import train_and_evaluate_models
        train_and_evaluate_models()
    with open(json_path, "r") as f:
        return json.load(f)

# Load data and models
df_cohort = load_cohort_data()
pipeline = load_model_pipeline()
metrics_metadata = load_model_metadata()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏛️ Sapthagiri NPS University")
    st.markdown("**Department of Computer Science & Engineering**")
    st.caption("Bengaluru, Karnataka, India | 2026–2027")
    st.markdown("---")

    nav_selection = st.radio(
        "Navigation Menu:",
        [
            "1. Dashboard",
            "2. Dataset Explorer",
            "3. Exploratory Data Analysis",
            "4. Model Training & Evaluation",
            "5. Student Performance Predictor",
            "6. Early Warning System",
            "7. Student Profiles",
            "8. About Project"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("##### 📌 Cohort Quick Facts")
    st.markdown(f"• **Students:** {len(df_cohort)}")
    st.markdown("• **Semester:** 5th Semester (B.E.)")
    st.markdown(f"• **Avg CGPA:** {df_cohort['Previous_CGPA'].mean():.2f} / 10.0")
    st.markdown(f"• **Avg Attendance:** {df_cohort['Attendance_Percentage'].mean():.1f}%")
    st.markdown(f"• **At-Risk Count:** {(df_cohort['Academic_Risk_Level'] == 'High Risk').sum()}")

    st.markdown("---")
    st.caption("EduPredict AI v2.0 • Data Mining and Data Wrangling")

# -----------------------------------------------------------------------------
# HELPER: HEADER BANNER
# -----------------------------------------------------------------------------
def render_header(title: str, subtitle: str):
    st.markdown(f"""
    <div class="univ-banner">
        <h1 class="univ-title">{title}</h1>
        <div class="univ-subtitle">{subtitle}</div>
        <div class="univ-meta">
            Sapthagiri NPS University, Bengaluru • Dept. of CSE • Academic Year 2026–2027 • 5th Semester
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# MODULE 1: UNIVERSITY ANALYTICS DASHBOARD
# =============================================================================
if nav_selection == "1. Dashboard":
    render_header(
        "Student Academic Performance Dashboard",
        "Executive Analytics and Continuous Academic Evaluation for 5th Semester CSE"
    )

    # Filter controls
    f_col1, f_col2, f_col3 = st.columns([1.2, 1.2, 1.6])
    with f_col1:
        sel_section = st.selectbox("Filter Section:", ["All Sections"] + sorted(list(df_cohort["Section"].unique())))
    with f_col2:
        sel_gender = st.selectbox("Filter Gender:", ["All Genders"] + sorted(list(df_cohort["Gender"].unique())))
    with f_col3:
        sel_cat = st.selectbox("Filter Performance:", ["All Categories"] + sorted(list(df_cohort["Predicted_Performance_Category"].unique())))

    df_filtered = df_cohort.copy()
    if sel_section != "All Sections":
        df_filtered = df_filtered[df_filtered["Section"] == sel_section]
    if sel_gender != "All Genders":
        df_filtered = df_filtered[df_filtered["Gender"] == sel_gender]
    if sel_cat != "All Categories":
        df_filtered = df_filtered[df_filtered["Predicted_Performance_Category"] == sel_cat]

    # KPI Metric Cards
    k1, k2, k3, k4, k5, k6, k7 = st.columns(7)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Cohort Size</div>
            <div class="kpi-value">{len(df_filtered)}</div>
            <div class="kpi-sub">Students</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg CGPA</div>
            <div class="kpi-value">{df_filtered['Previous_CGPA'].mean():.2f}</div>
            <div class="kpi-sub">Scale 0-10</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Attendance</div>
            <div class="kpi-value">{df_filtered['Attendance_Percentage'].mean():.1f}%</div>
            <div class="kpi-sub">Min 75% target</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Daily Study</div>
            <div class="kpi-value">{df_filtered['Daily_Study_Hours'].mean():.1f}h</div>
            <div class="kpi-sub">Self-study / day</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Avg Final Score</div>
            <div class="kpi-value">{df_filtered['Final_Score'].mean():.1f}</div>
            <div class="kpi-sub">Out of 100</div>
        </div>
        """, unsafe_allow_html=True)
    with k6:
        risk_count = (df_filtered['Academic_Risk_Level'] == 'High Risk').sum()
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #EF4444;">
            <div class="kpi-label">Academic Risk</div>
            <div class="kpi-value" style="color: #DC2626;">{risk_count}</div>
            <div class="kpi-sub">Needs Attention</div>
        </div>
        """, unsafe_allow_html=True)
    with k7:
        backlog_count = (df_filtered['Backlogs'] > 0).sum()
        st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid #F59E0B;">
            <div class="kpi-label">Backlogs</div>
            <div class="kpi-value" style="color: #D97706;">{backlog_count}</div>
            <div class="kpi-sub">Students with &gt;0</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Visualizations Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 1. Student Performance Category Distribution")
        cat_order = ["Excellent", "Very Good", "Good", "Average", "Needs Improvement"]
        cat_counts = df_filtered["Predicted_Performance_Category"].value_counts().reindex(cat_order).fillna(0).reset_index()
        cat_counts.columns = ["Category", "Count"]
        colors = ["#10B981", "#3B82F6", "#8B5CF6", "#F59E0B", "#EF4444"]
        fig1 = px.bar(
            cat_counts, x="Category", y="Count", color="Category",
            color_discrete_sequence=colors, text="Count"
        )
        fig1.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=340)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("##### 2. Section-wise Performance Distribution")
        fig2 = px.box(
            df_filtered, x="Section", y="Final_Score", color="Section",
            color_discrete_sequence=["#1E3A8A", "#6366F1", "#0D9488"],
            points="all"
        )
        fig2.update_layout(showlegend=False, margin=dict(l=20, r=20, t=30, b=20), height=340, yaxis_title="Final Score (0-100)")
        st.plotly_chart(fig2, use_container_width=True)

    # Visualizations Row 2
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("##### 3. Six 5th-Semester Subjects: Average Marks")
        subject_map = {
            "Marks_Mathematics": "Mathematics",
            "Marks_DSA": "DSA",
            "Marks_DBMS": "DBMS",
            "Marks_OS": "Operating Systems",
            "Marks_CN": "Computer Networks",
            "Marks_DMW": "Data Mining & Wrangling"
        }
        subj_means = df_filtered[list(subject_map.keys())].mean().rename(subject_map).reset_index()
        subj_means.columns = ["Subject", "Average Marks"]
        fig3 = px.bar(
            subj_means, x="Average Marks", y="Subject", orientation="h",
            color="Average Marks", color_continuous_scale="Blues", text_auto=".1f"
        )
        fig3.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340, coloraxis_showscale=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("##### 4. Attendance Percentage vs Final Performance Score")
        fig4 = px.scatter(
            df_filtered, x="Attendance_Percentage", y="Final_Score",
            color="Academic_Risk_Level",
            color_discrete_map={"Low Risk": "#10B981", "Medium Risk": "#F59E0B", "High Risk": "#EF4444"},
            hover_data=["Student_ID", "Student_Name", "Section", "Backlogs"],
            trendline="ols"
        )
        fig4.add_vline(x=75, line_dash="dash", line_color="red", annotation_text="Mandatory 75% Attendance")
        fig4.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340, xaxis_title="Attendance %", yaxis_title="Final Score (0-100)")
        st.plotly_chart(fig4, use_container_width=True)

    # Visualizations Row 3
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("##### 5. Daily Self-Study Hours vs Final Performance")
        fig5 = px.scatter(
            df_filtered, x="Daily_Study_Hours", y="Final_Score", color="Gender",
            color_discrete_sequence=["#2563EB", "#DB2777"],
            trendline="ols", hover_data=["Student_ID", "Student_Name"]
        )
        fig5.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340, xaxis_title="Daily Study Hours", yaxis_title="Final Score (0-100)")
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        st.markdown("##### 6. Backlog Frequency & Academic Risk Distribution")
        backlog_df = df_filtered.groupby(["Backlogs", "Academic_Risk_Level"]).size().reset_index(name="Student_Count")
        fig6 = px.bar(
            backlog_df, x="Backlogs", y="Student_Count", color="Academic_Risk_Level",
            barmode="stack", color_discrete_map={"Low Risk": "#10B981", "Medium Risk": "#F59E0B", "High Risk": "#EF4444"}
        )
        fig6.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340, yaxis_title="Number of Students")
        st.plotly_chart(fig6, use_container_width=True)


# =============================================================================
# MODULE 2: DATASET EXPLORER
# =============================================================================
elif nav_selection == "2. Dataset Explorer":
    render_header(
        "University Cohort Dataset Explorer",
        "Search, Filter, Inspect, and Export 5th Semester Student Records"
    )

    st.info("ℹ️ **Dataset Note:** This is a simulated demonstration dataset representing 300 undergraduate engineering students from Sapthagiri NPS University, Bengaluru for academic evaluation.")

    # Top search and filter row
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns([1.5, 1, 1, 1, 1])
    with col_s1:
        search_query = st.text_input("🔍 Search Student ID or Name:", placeholder="e.g., SNP012 or Vikram")
    with col_s2:
        sec_filt = st.selectbox("Section:", ["All"] + sorted(list(df_cohort["Section"].unique())))
    with col_s3:
        gen_filt = st.selectbox("Gender:", ["All"] + sorted(list(df_cohort["Gender"].unique())))
    with col_s4:
        cat_filt = st.selectbox("Performance Tier:", ["All"] + sorted(list(df_cohort["Predicted_Performance_Category"].unique())))
    with col_s5:
        sort_by = st.selectbox("Sort By:", ["Student_ID", "Previous_CGPA", "Final_Score", "Attendance_Percentage", "Backlogs"])

    # Row display limit
    col_l1, col_l2 = st.columns([2, 2])
    with col_l1:
        row_limit = st.radio("Display Row Limit:", [10, 50, 100, "All Records"], horizontal=True, index=1)

    # Filter logic
    df_view = df_cohort.copy()
    if search_query:
        df_view = df_view[
            df_view["Student_ID"].str.contains(search_query, case=False, na=False) |
            df_view["Student_Name"].str.contains(search_query, case=False, na=False)
        ]
    if sec_filt != "All":
        df_view = df_view[df_view["Section"] == sec_filt]
    if gen_filt != "All":
        df_view = df_view[df_view["Gender"] == gen_filt]
    if cat_filt != "All":
        df_view = df_view[df_view["Predicted_Performance_Category"] == cat_filt]

    df_view = df_view.sort_values(by=sort_by, ascending=(sort_by == "Student_ID"))

    if row_limit != "All Records":
        df_display = df_view.head(int(row_limit))
    else:
        df_display = df_view

    st.markdown(f"**Showing {len(df_display)} of {len(df_view)} matching student records** (Total Cohort: {len(df_cohort)})")
    st.dataframe(df_display, use_container_width=True)

    # Export Buttons
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        csv_filtered = df_view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Records (CSV)",
            data=csv_filtered,
            file_name="sapthagiri_students_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_d2:
        csv_full = df_cohort.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete 300-Student Dataset (CSV)",
            data=csv_full,
            file_name="sapthagiri_nps_university_students.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Attribute Data Dictionary
    with st.expander("📖 View Complete Attribute Definitions & Schema"):
        schema_data = [
            ("Student_ID", "String", "Unique university roll identifier (SNP001 to SNP300)"),
            ("Student_Name", "String", "Fictional realistic student name"),
            ("Department", "String", "Computer Science and Engineering"),
            ("Academic_Year", "String", "2026–2027"),
            ("Current_Semester", "String", "5th Semester"),
            ("Section", "Categorical", "Class partition: Section A, Section B, Section C"),
            ("Gender", "Binary", "Student gender (Male / Female)"),
            ("Age", "Integer", "Student age in completed years (19 - 22)"),
            ("Previous_CGPA", "Float", "Cumulative Grade Point Average from Semesters 1 to 4 (scale: 0.0 - 10.0)"),
            ("Attendance_Percentage", "Float", "Overall semester class attendance (scale: 0% - 100%)"),
            ("Absence_Days", "Integer", "Total days absent during the 5th semester"),
            ("Daily_Study_Hours", "Float", "Average self-study duration per day in hours"),
            ("Weekly_Library_Hours", "Float", "Library resource utilization hours per week"),
            ("Online_Learning_Hours", "Float", "Weekly hours spent on NPTEL/Coursera/online technical learning"),
            ("Assignment_Completion_Percentage", "Float", "Proportion of continuous internal lab & assignment submissions"),
            ("Internal_Assessment_Marks", "Float", "Average of Continuous Internal Evaluation (CIE) tests out of 100"),
            ("Previous_Semester_Performance", "Categorical", "Academic class standing (Distinction, First Class, Second Class, Pass, At Risk)"),
            ("Backlogs", "Integer", "Number of currently uncleared standing course backlogs"),
            ("Extracurricular_Participation", "Binary", "Active involvement in technical clubs, sports, or hackathons (Yes/No)"),
            ("Marks_Mathematics", "Float", "Advanced Engineering Mathematics assessment marks (0 - 100)"),
            ("Marks_DSA", "Float", "Data Structures and Algorithms marks (0 - 100)"),
            ("Marks_DBMS", "Float", "Database Management Systems marks (0 - 100)"),
            ("Marks_OS", "Float", "Operating Systems marks (0 - 100)"),
            ("Marks_CN", "Float", "Computer Networks marks (0 - 100)"),
            ("Marks_DMW", "Float", "Data Mining and Data Wrangling marks (0 - 100)"),
            ("Final_Score", "Float", "Target Variable: Final semester aggregate performance score (0 - 100)"),
            ("Predicted_Performance_Category", "Categorical", "Target Category (Excellent, Very Good, Good, Average, Needs Improvement)"),
            ("Academic_Risk_Level", "Categorical", "Early warning tier (Low Risk, Medium Risk, High Risk)")
        ]
        schema_df = pd.DataFrame(schema_data, columns=["Attribute Name", "Data Type", "Description & Academic Context"])
        st.table(schema_df)


# =============================================================================
# MODULE 3: EXPLORATORY DATA ANALYSIS (EDA)
# =============================================================================
elif nav_selection == "3. Exploratory Data Analysis":
    render_header(
        "Exploratory Data Analysis (EDA)",
        "Uncovering Multi-Dimensional Statistical Correlations in Student Performance"
    )

    tab1, tab2, tab3 = st.tabs(["📊 Distributions & Histograms", "📈 Attribute Correlations", "📚 Subject Performance Deep-Dive"])

    with tab1:
        st.subheader("1. Cohort Distribution Diagnostics")
        e_c1, e_c2 = st.columns(2)
        with e_c1:
            fig_cgpa = px.histogram(
                df_cohort, x="Previous_CGPA", nbins=20, marginal="box",
                color_discrete_sequence=["#1E3A8A"], title="CGPA Distribution (Semesters 1-4)"
            )
            fig_cgpa.update_layout(xaxis_title="CGPA (0 - 10)", yaxis_title="Student Count", height=350)
            st.plotly_chart(fig_cgpa, use_container_width=True)
            st.caption("💡 **Insight:** CGPA follows a normal distribution centered at 7.2. Students above 8.5 qualify for academic distinction.")

        with e_c2:
            fig_att = px.histogram(
                df_cohort, x="Attendance_Percentage", nbins=20, marginal="box",
                color_discrete_sequence=["#0D9488"], title="Attendance Percentage Distribution"
            )
            fig_att.add_vline(x=75, line_dash="dash", line_color="red", annotation_text="75% Mandatory")
            fig_att.update_layout(xaxis_title="Attendance %", yaxis_title="Student Count", height=350)
            st.plotly_chart(fig_att, use_container_width=True)
            st.caption("💡 **Insight:** Most students adhere to attendance regulations (> 75%), but a left tail of students (< 65%) faces academic debarment risk.")

        e_c3, e_c4 = st.columns(2)
        with e_c3:
            fig_study = px.histogram(
                df_cohort, x="Daily_Study_Hours", nbins=18,
                color="Section", color_discrete_sequence=["#3B82F6", "#6366F1", "#8B5CF6"],
                title="Daily Study Hours Distribution by Section"
            )
            fig_study.update_layout(xaxis_title="Hours / Day", yaxis_title="Student Count", height=350)
            st.plotly_chart(fig_study, use_container_width=True)
            st.caption("💡 **Insight:** Modal self-study time is approximately 2.5 to 3.5 hours per day across sections.")

        with e_c4:
            fig_final = px.histogram(
                df_cohort, x="Final_Score", nbins=22,
                color="Predicted_Performance_Category",
                color_discrete_map={"Excellent": "#10B981", "Very Good": "#3B82F6", "Good": "#8B5CF6", "Average": "#F59E0B", "Needs Improvement": "#EF4444"},
                title="Final Semester Performance Score Distribution"
            )
            fig_final.update_layout(xaxis_title="Final Score (0-100)", yaxis_title="Student Count", height=350)
            st.plotly_chart(fig_final, use_container_width=True)
            st.caption("💡 **Insight:** Demonstrates continuous performance spread across all performance classifications.")

    with tab2:
        st.subheader("2. Correlation Heatmap of Numerical Features")
        num_cols = [
            "Previous_CGPA", "Attendance_Percentage", "Daily_Study_Hours", "Weekly_Library_Hours",
            "Assignment_Completion_Percentage", "Internal_Assessment_Marks", "Backlogs",
            "Marks_Mathematics", "Marks_DSA", "Marks_DBMS", "Marks_OS", "Marks_CN", "Marks_DMW",
            "Final_Score"
        ]
        corr_matrix = df_cohort[num_cols].corr()

        fig_heat = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            color_continuous_scale="RdBu_r", title="Pearson Correlation Matrix (Academic, Behavioral & Target Variables)"
        )
        fig_heat.update_layout(height=650)
        st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("""
        **Key Empirical Takeaways from Correlation Analysis:**
        1. **Internal Assessment & Subject Marks ($r \approx 0.82$–$0.88$):** Formative continuous internal assessments have the strongest direct correlation with final semester outcomes.
        2. **Previous CGPA ($r \approx 0.74$):** Demonstrates longitudinal learning stability; prior academic consistency is a strong foundation.
        3. **Backlogs ($r \approx -0.58$):** Displays an inverse relationship; standing backlogs add cognitive load and divide attention during semester examinations.
        4. **Attendance & Study Hours ($r \approx 0.62$):** Positive behavioral indicators supporting exam preparedness.
        """)

    with tab3:
        st.subheader("3. Six Core 5th Semester Subjects: Comparative Analysis")
        subjects_df = df_cohort[[
            "Marks_Mathematics", "Marks_DSA", "Marks_DBMS",
            "Marks_OS", "Marks_CN", "Marks_DMW"
        ]].melt(var_name="Subject", value_name="Marks")

        subject_names_clean = {
            "Marks_Mathematics": "Mathematics",
            "Marks_DSA": "DSA",
            "Marks_DBMS": "DBMS",
            "Marks_OS": "Operating Systems",
            "Marks_CN": "Computer Networks",
            "Marks_DMW": "Data Mining & Wrangling"
        }
        subjects_df["Subject"] = subjects_df["Subject"].map(subject_names_clean)

        fig_box = px.box(
            subjects_df, x="Subject", y="Marks", color="Subject",
            points="outliers", title="Grade Distribution and Variance Across 6 Subjects"
        )
        fig_box.update_layout(height=420, showlegend=False, yaxis_title="Marks (0 - 100)")
        st.plotly_chart(fig_box, use_container_width=True)

        st.caption("💡 **Subject Rigor Insight:** Mathematics and Data Structures & Algorithms demonstrate higher variance and lower median scores, pinpointing them as key targets for remedial coaching.")


# =============================================================================
# MODULE 4: MODEL TRAINING & EVALUATION
# =============================================================================
elif nav_selection == "4. Model Training & Evaluation":
    render_header(
        "Machine Learning Model Benchmark & Comparison",
        "Rigorous Evaluation of Supervised Regression Algorithms (80/20 Test Partition)"
    )

    results = metrics_metadata["metrics"]
    metrics_df = pd.DataFrame(results).T
    best_name = metrics_metadata["best_model_name"]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Winning Model", best_name)
    with m2:
        st.metric("Lowest Test RMSE", f"{results[best_name]['RMSE']:.4f}")
    with m3:
        st.metric("Lowest Test MAE", f"{results[best_name]['MAE']:.4f}")
    with m4:
        st.metric("Variance Explained (R²)", f"{results[best_name]['R2'] * 100:.2f}%")

    st.markdown("### 📊 Experimental Comparison Table (Held-Out 20% Test Partition)")
    st.table(metrics_df.style.format("{:.4f}"))

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("##### MAE vs RMSE (Lower is Better)")
        fig_err = go.Figure(data=[
            go.Bar(name='MAE', x=metrics_df.index, y=metrics_df['MAE'], marker_color='#3B82F6'),
            go.Bar(name='RMSE', x=metrics_df.index, y=metrics_df['RMSE'], marker_color='#1E3A8A')
        ])
        fig_err.update_layout(barmode='group', height=360, margin=dict(l=20, r=20, t=30, b=20), yaxis_title="Error Points (0-100 scale)")
        st.plotly_chart(fig_err, use_container_width=True)

    with col_g2:
        st.markdown("##### Coefficient of Determination R² (Higher is Better)")
        fig_r2 = px.bar(
            metrics_df.reset_index(), x="index", y="R2",
            color="R2", color_continuous_scale="Greens", text_auto=".4f"
        )
        fig_r2.update_layout(height=360, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Algorithm", yaxis_title="R² Score", coloraxis_showscale=False)
        st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("### 🌟 Feature Importance Ranking (Primary Drivers of Academic Success)")
    feat_df = pd.DataFrame(metrics_metadata["feature_importances"])
    fig_feat = px.bar(
        feat_df, x="importance", y="feature", orientation="h",
        color="importance", color_continuous_scale="Purples"
    )
    fig_feat.update_layout(height=420, yaxis=dict(autorange="reversed"), xaxis_title="Relative Weight / Importance", coloraxis_showscale=False)
    st.plotly_chart(fig_feat, use_container_width=True)

    st.info("💡 **Methodology Verification:** The machine learning pipeline applies zero target leakage. All numerical features are scaled using `StandardScaler` and categorical attributes are encoded with `OneHotEncoder`, fitted strictly on the 80% training partition ($N=240$).")


# =============================================================================
# MODULE 5: STUDENT PERFORMANCE PREDICTOR
# =============================================================================
elif nav_selection == "5. Student Performance Predictor":
    render_header(
        "Student Performance Predictor & Counseling Tool",
        "Forecast Academic Outcomes and Generate Actionable Guidance"
    )

    st.markdown("Enter student academic metrics, attendance, and study habits to predict final performance:")

    with st.form("univ_prediction_form"):
        st.markdown("#### 1. Formative Internal Marks (Six Core 5th Semester Subjects)")
        sm1, sm2, sm3 = st.columns(3)
        with sm1:
            in_math = st.slider("Mathematics Marks (0-100):", 0, 100, 72)
            in_dsa = st.slider("Data Structures & Algorithms Marks (0-100):", 0, 100, 74)
        with sm2:
            in_dbms = st.slider("DBMS Marks (0-100):", 0, 100, 80)
            in_os = st.slider("Operating Systems Marks (0-100):", 0, 100, 75)
        with sm3:
            in_cn = st.slider("Computer Networks Marks (0-100):", 0, 100, 78)
            in_dmw = st.slider("Data Mining & Data Wrangling Marks (0-100):", 0, 100, 82)

        st.markdown("#### 2. Academic History & Continuous Evaluation")
        ah1, ah2, ah3, ah4 = st.columns(4)
        with ah1:
            in_cgpa = st.number_input("Previous CGPA (Sem 1-4):", min_value=0.0, max_value=10.0, value=7.65, step=0.05)
        with ah2:
            in_cie = st.slider("Internal Assessment (CIE) Average:", 0, 100, 76)
        with ah3:
            in_backlogs = st.selectbox("Active Backlogs:", [0, 1, 2, 3, 4], index=0)
        with ah4:
            in_prev_class = st.selectbox("Previous Sem Standing:", ["Distinction", "First Class", "Second Class", "Pass Class", "At Risk"], index=1)

        st.markdown("#### 3. Attendance, Study Habits & Learning Engagement")
        sh1, sh2, sh3, sh4 = st.columns(4)
        with sh1:
            in_att = st.slider("Attendance Percentage (%):", 30.0, 100.0, 84.0, step=0.5)
            in_abs = int(round((100.0 - in_att) * 0.45))
        with sh2:
            in_study = st.slider("Daily Self-Study (Hours):", 0.5, 10.0, 3.0, step=0.5)
        with sh3:
            in_lib = st.slider("Weekly Library Hours:", 0.0, 20.0, 4.0, step=0.5)
        with sh4:
            in_assign = st.slider("Assignment Completion (%):", 20.0, 100.0, 88.0, step=1.0)

        st.markdown("#### 4. Demographics & Class Section")
        dm1, dm2, dm3, dm4 = st.columns(4)
        with dm1:
            in_sec = st.selectbox("Section:", ["Section A", "Section B", "Section C"], index=0)
        with dm2:
            in_gen = st.selectbox("Gender:", ["Female", "Male"], index=0)
        with dm3:
            in_age = st.selectbox("Age:", [19, 20, 21, 22], index=1)
        with dm4:
            in_extra = st.selectbox("Extracurricular Activity:", ["Yes", "No"], index=0)

        predict_button = st.form_submit_button("🔮 Predict Student Academic Performance", use_container_width=True)

    if predict_button:
        student_input = {
            'Section': in_sec,
            'Gender': in_gen,
            'Previous_Semester_Performance': in_prev_class,
            'Extracurricular_Participation': in_extra,
            'Age': in_age,
            'Previous_CGPA': in_cgpa,
            'Attendance_Percentage': in_att,
            'Absence_Days': in_abs,
            'Daily_Study_Hours': in_study,
            'Weekly_Library_Hours': in_lib,
            'Online_Learning_Hours': 4.0,
            'Assignment_Completion_Percentage': in_assign,
            'Internal_Assessment_Marks': in_cie,
            'Backlogs': in_backlogs,
            'Marks_Mathematics': in_math,
            'Marks_DSA': in_dsa,
            'Marks_DBMS': in_dbms,
            'Marks_OS': in_os,
            'Marks_CN': in_cn,
            'Marks_DMW': in_dmw
        }

        from predict import predict_student_performance
        prediction_output = predict_student_performance(student_input, pipeline=pipeline)

        score = prediction_output["final_score"]
        category = prediction_output["performance_category"]
        risk = prediction_output["academic_risk_level"]
        recommendations = prediction_output["recommendations"]

        st.markdown("---")
        st.subheader("🎓 Prediction Results & Evaluation")

        r_col1, r_col2, r_col3 = st.columns([1.2, 1.2, 1.6])
        with r_col1:
            st.metric("Predicted Final Score", f"{score:.2f} / 100")
        with r_col2:
            if category == "Excellent":
                badge_html = "<div class='badge-excellent'>🌟 Excellent (85–100)</div>"
            elif category == "Very Good":
                badge_html = "<div class='badge-verygood'>✅ Very Good (70–84)</div>"
            elif category == "Good":
                badge_html = "<div class='badge-good'>📘 Good (60–69)</div>"
            elif category == "Average":
                badge_html = "<div class='badge-average'>⚠️ Average (50–59)</div>"
            else:
                badge_html = "<div class='badge-risk'>🚨 Needs Improvement (&lt; 50)</div>"
            st.markdown(f"**Performance Tier:**<br>{badge_html}", unsafe_allow_html=True)

        with r_col3:
            if risk == "Low Risk":
                risk_badge = "<div class='badge-excellent'>🟢 Low Academic Risk</div>"
            elif risk == "Medium Risk":
                risk_badge = "<div class='badge-average'>🟡 Medium Academic Risk</div>"
            else:
                risk_badge = "<div class='badge-risk'>🔴 High Academic Risk</div>"
            st.markdown(f"**Early Warning Status:**<br>{risk_badge}", unsafe_allow_html=True)

        # Progress / Performance Meter
        st.markdown("#### Performance Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Predicted Final Semester Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1E3A8A"},
                'steps': [
                    {'range': [0, 50], 'color': "#FEE2E2"},
                    {'range': [50, 60], 'color': "#FEF3C7"},
                    {'range': [60, 70], 'color': "#EDE9FE"},
                    {'range': [70, 85], 'color': "#DBEAFE"},
                    {'range': [85, 100], 'color': "#D1FAE5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 3},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        fig_gauge.update_layout(height=280, margin=dict(l=30, r=30, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        st.markdown("#### 📋 Actionable Academic Counseling Recommendations")
        for rec in recommendations:
            st.markdown(f"• {rec}")


# =============================================================================
# MODULE 6: EARLY ACADEMIC WARNING SYSTEM
# =============================================================================
elif nav_selection == "6. Early Warning System":
    render_header(
        "Early Academic Warning & Student Support System",
        "Proactive Identification of At-Risk Students for Academic Counseling and Mentorship"
    )

    st.markdown("""
    This module identifies students needing academic intervention based on **attendance records**, **backlog counts**, and **predicted performance**.
    > ⚠️ **Academic Policy Notice:** In accordance with university standards, attendance below 75% triggers attendance warnings, and below 65% triggers exam debarment review.
    """)

    # Filter Risk Tiers
    f_risk = st.radio("Filter by Risk Category:", ["All Tiers", "High Risk", "Medium Risk", "Low Risk"], horizontal=True, index=1)

    df_risk_view = df_cohort.copy()
    if f_risk != "All Tiers":
        df_risk_view = df_risk_view[df_risk_view["Academic_Risk_Level"] == f_risk]

    # Metrics row
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric("Total Flagged", len(df_risk_view))
    with r2:
        st.metric("Avg Attendance", f"{df_risk_view['Attendance_Percentage'].mean():.1f}%")
    with r3:
        st.metric("Avg Backlogs", f"{df_risk_view['Backlogs'].mean():.1f}")
    with r4:
        st.metric("Avg Predicted Score", f"{df_risk_view['Final_Score'].mean():.1f} / 100")

    # Table columns
    risk_cols = [
        "Student_ID", "Student_Name", "Section", "Previous_CGPA",
        "Attendance_Percentage", "Backlogs", "Final_Score",
        "Predicted_Performance_Category", "Academic_Risk_Level"
    ]
    st.dataframe(df_risk_view[risk_cols].sort_values(by="Final_Score"), use_container_width=True)

    # Download action list
    csv_risk = df_risk_view[risk_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Early Warning Roster (CSV for HOD & Mentors)",
        data=csv_risk,
        file_name="sapthagiri_early_warning_roster.csv",
        mime="text/csv"
    )

    st.markdown("### Recommended Academic Action Protocol")
    st.markdown("""
    | Risk Tier | Criteria | Mandatory Action |
    | :--- | :--- | :--- |
    | **🔴 High Risk** | Final Score $< 50$, Attendance $< 65\%$, or $\ge 3$ Backlogs | Immediate parent-teacher meeting, mandatory remedial coaching, weekly attendance monitoring. |
    | **🟡 Medium Risk** | Final Score $50 - 59$, Attendance $65 - 74\%$, or $2$ Backlogs | Department faculty mentor counseling, assignment completion recovery plan, peer tutoring. |
    | **🟢 Low Risk** | Final Score $\ge 60$, Attendance $\ge 75\%$, $\le 1$ Backlogs | Standard academic progress tracking; encourage research and hackathon participation. |
    """)


# =============================================================================
# MODULE 7: INDIVIDUAL STUDENT PROFILES
# =============================================================================
elif nav_selection == "7. Student Profiles":
    render_header(
        "Individual Student Academic Profile",
        "Comprehensive Student Performance Record and Subject Competency Analysis"
    )

    # Selector
    student_list = df_cohort["Student_ID"] + " - " + df_cohort["Student_Name"]
    selected_entry = st.selectbox("Select Student to Inspect:", student_list)
    sel_id = selected_entry.split(" - ")[0]

    student_record = df_cohort[df_cohort["Student_ID"] == sel_id].iloc[0]

    # Student Card Layout
    prof_col1, prof_col2, prof_col3 = st.columns([1, 1.5, 1.5])

    with prof_col1:
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 18px; text-align: center;">
            <div style="font-size: 3rem;">🎓</div>
            <h3 style="margin: 6px 0; color: #1E3A8A;">{student_record['Student_Name']}</h3>
            <div style="font-weight: 600; color: #64748B;">{student_record['Student_ID']}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">{student_record['Department']}</div>
            <div style="margin-top: 10px;">
                <span class="badge-good">{student_record['Section']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with prof_col2:
        st.markdown("##### Academic Vital Metrics")
        st.markdown(f"• **Previous CGPA:** `{student_record['Previous_CGPA']:.2f} / 10.0`")
        st.markdown(f"• **Class Attendance:** `{student_record['Attendance_Percentage']:.1f}%` ({student_record['Absence_Days']} days absent)")
        st.markdown(f"• **Daily Self-Study:** `{student_record['Daily_Study_Hours']} hours/day`")
        st.markdown(f"• **Library Usage:** `{student_record['Weekly_Library_Hours']} hours/week`")
        st.markdown(f"• **Active Backlogs:** `{student_record['Backlogs']}`")

    with prof_col3:
        st.markdown("##### Prediction Assessment")
        st.markdown(f"• **Predicted Final Score:** `{student_record['Final_Score']:.2f} / 100`")
        st.markdown(f"• **Performance Category:** `{student_record['Predicted_Performance_Category']}`")
        st.markdown(f"• **Risk Evaluation:** `{student_record['Academic_Risk_Level']}`")
        st.markdown(f"• **Extracurricular Activities:** `{student_record['Extracurricular_Participation']}`")
        st.markdown(f"• **Internal Assessment CIE:** `{student_record['Internal_Assessment_Marks']:.1f} / 100`")

    st.markdown("---")

    # Subject Radar / Bar Chart Comparison
    subj_keys = ['Marks_Mathematics', 'Marks_DSA', 'Marks_DBMS', 'Marks_OS', 'Marks_CN', 'Marks_DMW']
    subj_labels = ['Mathematics', 'DSA', 'DBMS', 'Operating Systems', 'Computer Networks', 'Data Mining']

    student_marks = [float(student_record[k]) for k in subj_keys]
    cohort_avg = [float(df_cohort[k].mean()) for k in subj_keys]

    fig_subj = go.Figure()
    fig_subj.add_trace(go.Bar(
        x=subj_labels, y=student_marks, name=f"{student_record['Student_Name']} Marks", marker_color='#1E3A8A'
    ))
    fig_subj.add_trace(go.Bar(
        x=subj_labels, y=cohort_avg, name="Cohort Average", marker_color='#94A3B8'
    ))
    fig_subj.update_layout(
        title=f"Subject Marks Comparison for {student_record['Student_Name']} vs Cohort Average",
        barmode='group', height=360, yaxis_title="Marks (0 - 100)"
    )
    st.plotly_chart(fig_subj, use_container_width=True)


# =============================================================================
# MODULE 8: ABOUT PROJECT & DOCUMENTATION
# =============================================================================
elif nav_selection == "8. About Project":
    render_header(
        "About EduPredict AI",
        "Project Architecture, Academic Specifications, and Methodology Documentation"
    )

    st.markdown("""
    ### 🏛️ Institutional Information
    * **University:** Sapthagiri NPS University, Bengaluru, Karnataka, India
    * **Department:** Department of Computer Science and Engineering
    * **Academic Year:** 2026–2027
    * **Program:** Bachelor of Engineering (B.E.), 5th Semester
    * **Course:** Data Mining and Data Wrangling
    * **Developer:** Rudresh Swamy

    ---

    ### 🎯 Problem Statement
    Traditional academic performance evaluation is reactive—educators discover student failure only after semester examinations conclude, missing the crucial window for remedial intervention. EduPredict AI creates a proactive early-warning decision-support mechanism by predicting continuous final examination outcomes from formative internal assessments, attendance patterns, and study habits.

    ---

    ### 📊 Dataset Description & Disclaimer
    * **Cohort Size:** 300 undergraduate engineering students from the 5th semester Computer Science & Engineering department.
    * **Attributes:** 28 variables spanning demographics, attendance, study habits, backlogs, and six core 5th-semester subjects:
      1. Advanced Engineering Mathematics
      2. Data Structures and Algorithms
      3. Database Management Systems
      4. Operating Systems
      5. Computer Networks
      6. Data Mining and Data Wrangling
    * **⚠️ Academic Disclaimer:** This dataset is a synthesized cohort designed specifically for academic evaluation and machine learning benchmarking at Sapthagiri NPS University. It does not contain private or unauthorized student personal records.

    ---

    ### 🤖 Machine Learning Pipeline & Empirical Results
    * **Data Leakage Prevention:** Preprocessing steps (`StandardScaler` on continuous features, `OneHotEncoder` on nominal categories) are executed inside Scikit-Learn `Pipeline` architectures fitted exclusively on the 80% training partition ($N=240$).
    * **Algorithms Benchmarked:**
      * **Linear Regression:** Baseline parametric regression ($R^2 \approx 0.9277$, $\text{RMSE} \approx 3.37$)
      * **Decision Tree Regressor:** Non-linear decision rules ($R^2 \approx 0.7918$, $\text{RMSE} \approx 5.72$)
      * **Random Forest Regressor:** Bootstrap ensemble of 120 decorrelated decision trees ($R^2 \approx 0.9039$, $\text{RMSE} \approx 3.89$)
    * **Evaluation Metrics:** Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and Coefficient of Determination ($R^2$).
    * **Serialization:** Model artifacts are serialized with `joblib` for real-time inference without retraining latency.
    """)
