"""
================================================================================
EduPredict AI: Native Windows Desktop Application
Institution : Sapthagiri NPS University, Bengaluru, Karnataka, India
Department  : Department of Computer Science and Engineering
Academic Yr : 2026–2027 | Undergraduate Engineering (5th Semester)
Technology  : Python Tkinter / ttk Native Desktop GUI
================================================================================
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import joblib

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from predict import predict_student_performance

class EduPredictDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EduPredict AI - Sapthagiri NPS University")
        self.geometry("1100x750")
        self.minsize(950, 650)
        
        # Load resources
        self.data_path = os.path.join(CURRENT_DIR, "dataset", "university_students.csv")
        self.model_path = os.path.join(CURRENT_DIR, "model", "best_model.joblib")
        
        if os.path.exists(self.data_path):
            self.df = pd.read_csv(self.data_path)
        else:
            messagebox.showerror("Error", f"Dataset not found at {self.data_path}")
            self.df = pd.DataFrame()

        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            self.pipeline = None

        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except:
            pass

        # Color definitions
        self.NAVY = "#1E3A8A"
        self.DARK_NAVY = "#0F172A"
        self.ACCENT_PURPLE = "#4F46E5"
        self.LIGHT_BG = "#F8FAFC"
        self.CARD_BG = "#FFFFFF"

        self.configure(bg=self.LIGHT_BG)
        self.style.configure(".", font=("Segoe UI", 10))
        self.style.configure("TNotebook", background=self.LIGHT_BG)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[16, 8])
        self.style.map("TNotebook.Tab", background=[("selected", self.NAVY)], foreground=[("selected", "white")])

    def build_ui(self):
        # 1. Header Banner
        header = tk.Frame(self, bg=self.DARK_NAVY, height=80)
        header.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header,
            text="🏛️ SAPTHAGIRI NPS UNIVERSITY, BENGALURU",
            font=("Segoe UI", 14, "bold"),
            fg="#FFFFFF",
            bg=self.DARK_NAVY
        )
        title_lbl.pack(anchor="w", padx=20, pady=(12, 2))

        sub_lbl = tk.Label(
            header,
            text="Department of Computer Science & Engineering • EduPredict AI Desktop Application (5th Sem B.E.)",
            font=("Segoe UI", 9),
            fg="#CBD5E1",
            bg=self.DARK_NAVY
        )
        sub_lbl.pack(anchor="w", padx=20, pady=(0, 12))

        # 2. Main Tabs Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)

        # Build each tab
        self.tab_dashboard = tk.Frame(self.notebook, bg=self.LIGHT_BG)
        self.tab_predictor = tk.Frame(self.notebook, bg=self.LIGHT_BG)
        self.tab_warning = tk.Frame(self.notebook, bg=self.LIGHT_BG)
        self.tab_profile = tk.Frame(self.notebook, bg=self.LIGHT_BG)

        self.notebook.add(self.tab_dashboard, text="📊 Dashboard & KPIs")
        self.notebook.add(self.tab_predictor, text="🎯 Performance Predictor")
        self.notebook.add(self.tab_warning, text="🚨 Early Warning System")
        self.notebook.add(self.tab_profile, text="🔍 Student Profiles")

        self.build_dashboard_tab()
        self.build_predictor_tab()
        self.build_warning_tab()
        self.build_profile_tab()

    # -------------------------------------------------------------------------
    # TAB 1: DASHBOARD
    # -------------------------------------------------------------------------
    def build_dashboard_tab(self):
        pad = tk.Frame(self.tab_dashboard, bg=self.LIGHT_BG)
        pad.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        tk.Label(pad, text="5th Semester CSE Cohort Overview (300 Students)", font=("Segoe UI", 13, "bold"), fg=self.NAVY, bg=self.LIGHT_BG).pack(anchor="w", pady=(0, 12))

        # KPI Row
        kpi_frame = tk.Frame(pad, bg=self.LIGHT_BG)
        kpi_frame.pack(fill=tk.X, pady=(0, 20))

        if not self.df.empty:
            total_students = len(self.df)
            avg_cgpa = f"{self.df['Previous_CGPA'].mean():.2f}"
            avg_att = f"{self.df['Attendance_Percentage'].mean():.1f}%"
            avg_score = f"{self.df['Final_Score'].mean():.1f}"
            risk_count = int((self.df['Academic_Risk_Level'] == 'High Risk').sum())
        else:
            total_students, avg_cgpa, avg_att, avg_score, risk_count = 0, "0", "0%", "0", 0

        kpis = [
            ("TOTAL COHORT", str(total_students), "#1E3A8A"),
            ("AVERAGE CGPA", avg_cgpa, "#0D9488"),
            ("AVG ATTENDANCE", avg_att, "#2563EB"),
            ("AVG FINAL SCORE", avg_score, "#4F46E5"),
            ("AT-RISK STUDENTS", str(risk_count), "#DC2626")
        ]

        for title, val, color in kpis:
            card = tk.Frame(kpi_frame, bg="white", relief="solid", bd=1, padx=15, pady=12)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6)
            tk.Label(card, text=title, font=("Segoe UI", 8, "bold"), fg="#64748B", bg="white").pack()
            tk.Label(card, text=val, font=("Segoe UI", 18, "bold"), fg=color, bg="white").pack(pady=4)

        # Subject Averages Table
        subj_frame = tk.LabelFrame(pad, text="Six Core Academic Subjects: 5th Semester Average Marks", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=12)
        subj_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        cols = ("Subject", "Average Marks (0-100)", "Status")
        tree = ttk.Treeview(subj_frame, columns=cols, show="headings", height=6)
        tree.heading("Subject", text="Subject")
        tree.heading("Average Marks (0-100)", text="Average Marks (0-100)")
        tree.heading("Status", text="Status")
        tree.column("Subject", width=350)
        tree.column("Average Marks (0-100)", width=200, anchor="center")
        tree.column("Status", width=180, anchor="center")

        subjects = [
            ("Mathematics (Engineering Mathematics & Discrete)", "Marks_Mathematics"),
            ("Data Structures & Algorithms", "Marks_DSA"),
            ("Database Management Systems", "Marks_DBMS"),
            ("Operating Systems", "Marks_OS"),
            ("Computer Networks", "Marks_CN"),
            ("Data Mining & Data Wrangling", "Marks_DMW")
        ]

        for s_name, col_name in subjects:
            if not self.df.empty and col_name in self.df.columns:
                m_avg = self.df[col_name].mean()
                status = "Satisfactory" if m_avg >= 60 else "Attention Needed"
                tree.insert("", tk.END, values=(s_name, f"{m_avg:.1f} / 100", status))

        tree.pack(fill=tk.BOTH, expand=True)

    # -------------------------------------------------------------------------
    # TAB 2: PREDICTOR
    # -------------------------------------------------------------------------
    def build_predictor_tab(self):
        canvas = tk.Canvas(self.tab_predictor, bg=self.LIGHT_BG, highlightthickness=0)
        scroll = ttk.Scrollbar(self.tab_predictor, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=self.LIGHT_BG)

        form_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        scroll.pack(side="right", fill="y")

        tk.Label(form_frame, text="Enter Student Academic Information for Performance Forecasting:", font=("Segoe UI", 11, "bold"), fg=self.NAVY, bg=self.LIGHT_BG).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

        # Subjects
        tk.Label(form_frame, text="1. Core Subject Internal Marks (0-100):", font=("Segoe UI", 10, "bold"), bg=self.LIGHT_BG).grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 5))

        self.in_math = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Mathematics", length=220, bg=self.LIGHT_BG)
        self.in_math.set(75)
        self.in_math.grid(row=2, column=0, padx=8, pady=4)

        self.in_dsa = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Data Structures & Algorithms", length=220, bg=self.LIGHT_BG)
        self.in_dsa.set(72)
        self.in_dsa.grid(row=2, column=1, padx=8, pady=4)

        self.in_dbms = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="DBMS", length=220, bg=self.LIGHT_BG)
        self.in_dbms.set(80)
        self.in_dbms.grid(row=2, column=2, padx=8, pady=4)

        self.in_os = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Operating Systems", length=220, bg=self.LIGHT_BG)
        self.in_os.set(74)
        self.in_os.grid(row=3, column=0, padx=8, pady=4)

        self.in_cn = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Computer Networks", length=220, bg=self.LIGHT_BG)
        self.in_cn.set(78)
        self.in_cn.grid(row=3, column=1, padx=8, pady=4)

        self.in_dmw = tk.Scale(form_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Data Mining & Wrangling", length=220, bg=self.LIGHT_BG)
        self.in_dmw.set(82)
        self.in_dmw.grid(row=3, column=2, padx=8, pady=4)

        # Academic & Study Metrics
        tk.Label(form_frame, text="2. Academic History & Study Habits:", font=("Segoe UI", 10, "bold"), bg=self.LIGHT_BG).grid(row=4, column=0, columnspan=4, sticky="w", pady=(15, 5))

        self.in_cgpa = tk.Scale(form_frame, from_=4.0, to=10.0, resolution=0.1, orient=tk.HORIZONTAL, label="Previous CGPA (Sem 1-4)", length=220, bg=self.LIGHT_BG)
        self.in_cgpa.set(7.5)
        self.in_cgpa.grid(row=5, column=0, padx=8, pady=4)

        self.in_att = tk.Scale(form_frame, from_=40, to=100, orient=tk.HORIZONTAL, label="Attendance Percentage (%)", length=220, bg=self.LIGHT_BG)
        self.in_att.set(85)
        self.in_att.grid(row=5, column=1, padx=8, pady=4)

        self.in_study = tk.Scale(form_frame, from_=1.0, to=8.0, resolution=0.5, orient=tk.HORIZONTAL, label="Daily Study Hours", length=220, bg=self.LIGHT_BG)
        self.in_study.set(3.0)
        self.in_study.grid(row=5, column=2, padx=8, pady=4)

        # Backlogs and Section
        f_sub = tk.Frame(form_frame, bg=self.LIGHT_BG)
        f_sub.grid(row=6, column=0, columnspan=3, sticky="w", padx=8, pady=10)

        tk.Label(f_sub, text="Active Backlogs:", bg=self.LIGHT_BG, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        self.in_backlogs = ttk.Combobox(f_sub, values=[0, 1, 2, 3, 4], width=5, state="readonly")
        self.in_backlogs.set(0)
        self.in_backlogs.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(f_sub, text="Section:", bg=self.LIGHT_BG, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        self.in_sec = ttk.Combobox(f_sub, values=["Section A", "Section B", "Section C"], width=12, state="readonly")
        self.in_sec.set("Section A")
        self.in_sec.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(f_sub, text="Gender:", bg=self.LIGHT_BG, font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        self.in_gen = ttk.Combobox(f_sub, values=["Female", "Male"], width=10, state="readonly")
        self.in_gen.set("Female")
        self.in_gen.pack(side=tk.LEFT)

        # Predict Button
        btn = tk.Button(form_frame, text="🔮 PREDICT ACADEMIC PERFORMANCE", font=("Segoe UI", 11, "bold"), bg=self.NAVY, fg="white", padx=20, pady=8, cursor="hand2", command=self.on_predict)
        btn.grid(row=7, column=0, columnspan=3, pady=(15, 10))

        # Result Display Area
        self.res_frame = tk.LabelFrame(form_frame, text="Prediction & Counseling Outcome", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=12)
        self.res_frame.grid(row=8, column=0, columnspan=3, sticky="ew", padx=8, pady=(10, 25))

        self.res_score_lbl = tk.Label(self.res_frame, text="Predicted Final Score: -- / 100", font=("Segoe UI", 13, "bold"), fg=self.NAVY, bg="white")
        self.res_score_lbl.pack(anchor="w")

        self.res_tier_lbl = tk.Label(self.res_frame, text="Performance Tier: --", font=("Segoe UI", 11, "bold"), fg="#10B981", bg="white")
        self.res_tier_lbl.pack(anchor="w", pady=2)

        self.res_risk_lbl = tk.Label(self.res_frame, text="Academic Risk Level: --", font=("Segoe UI", 11, "bold"), fg="#2563EB", bg="white")
        self.res_risk_lbl.pack(anchor="w", pady=2)

        self.res_rec_text = tk.Text(self.res_frame, height=5, width=90, font=("Segoe UI", 9), wrap=tk.WORD, relief="solid", bd=1)
        self.res_rec_text.pack(fill=tk.BOTH, pady=(8, 4))
        self.res_rec_text.insert(tk.END, "Personalized academic counseling suggestions will appear here after clicking Predict.")
        self.res_rec_text.config(state=tk.DISABLED)

    def on_predict(self):
        try:
            student_dict = {
                'Section': self.in_sec.get(),
                'Gender': self.in_gen.get(),
                'Previous_Semester_Performance': 'First Class',
                'Extracurricular_Participation': 'Yes',
                'Age': 20,
                'Previous_CGPA': float(self.in_cgpa.get()),
                'Attendance_Percentage': float(self.in_att.get()),
                'Absence_Days': int(round((100.0 - float(self.in_att.get())) * 0.45)),
                'Daily_Study_Hours': float(self.in_study.get()),
                'Weekly_Library_Hours': 3.5,
                'Online_Learning_Hours': 4.0,
                'Assignment_Completion_Percentage': 85.0,
                'Internal_Assessment_Marks': (self.in_math.get() + self.in_dsa.get() + self.in_dbms.get()) / 3.0,
                'Backlogs': int(self.in_backlogs.get()),
                'Marks_Mathematics': float(self.in_math.get()),
                'Marks_DSA': float(self.in_dsa.get()),
                'Marks_DBMS': float(self.in_dbms.get()),
                'Marks_OS': float(self.in_os.get()),
                'Marks_CN': float(self.in_cn.get()),
                'Marks_DMW': float(self.in_dmw.get())
            }

            result = predict_student_performance(student_dict, pipeline=self.pipeline)
            score = result["final_score"]
            cat = result["performance_category"]
            risk = result["academic_risk_level"]

            self.res_score_lbl.config(text=f"Predicted Final Score: {score:.2f} / 100")
            self.res_tier_lbl.config(text=f"Performance Tier: {cat}")
            self.res_risk_lbl.config(text=f"Academic Risk Level: {risk}")

            if risk == "High Risk":
                self.res_risk_lbl.config(fg="#DC2626")
            elif risk == "Medium Risk":
                self.res_risk_lbl.config(fg="#D97706")
            else:
                self.res_risk_lbl.config(fg="#16A34A")

            self.res_rec_text.config(state=tk.NORMAL)
            self.res_rec_text.delete(1.0, tk.END)
            for r in result["recommendations"]:
                self.res_rec_text.insert(tk.END, f"• {r}\n")
            self.res_rec_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Prediction Error", str(e))

    # -------------------------------------------------------------------------
    # TAB 3: EARLY WARNING SYSTEM
    # -------------------------------------------------------------------------
    def build_warning_tab(self):
        frame = tk.Frame(self.tab_warning, bg=self.LIGHT_BG, padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Students Requiring Academic Mentorship & Intervention", font=("Segoe UI", 12, "bold"), fg=self.NAVY, bg=self.LIGHT_BG).pack(anchor="w", pady=(0, 8))

        # Filter buttons
        btn_box = tk.Frame(frame, bg=self.LIGHT_BG)
        btn_box.pack(anchor="w", pady=(0, 10))

        tk.Button(btn_box, text="All Risk Tiers", command=lambda: self.load_warning_table("All"), padx=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="🔴 High Risk Only", bg="#FEE2E2", fg="#991B1B", command=lambda: self.load_warning_table("High Risk"), padx=10).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="🟡 Medium Risk Only", bg="#FEF3C7", fg="#92400E", command=lambda: self.load_warning_table("Medium Risk"), padx=10).pack(side=tk.LEFT, padx=3)

        cols = ("Student_ID", "Student_Name", "Section", "CGPA", "Attendance", "Backlogs", "Final Score", "Risk Tier")
        self.warn_tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.warn_tree.heading(c, text=c)
            self.warn_tree.column(c, width=110, anchor="center")
        self.warn_tree.column("Student_Name", width=180, anchor="w")

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.warn_tree.yview)
        self.warn_tree.configure(yscrollcommand=scroll_y.set)

        self.warn_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_warning_table("All")

    def load_warning_table(self, risk_tier="All"):
        for item in self.warn_tree.get_children():
            self.warn_tree.delete(item)

        if self.df.empty:
            return

        df_sub = self.df if risk_tier == "All" else self.df[self.df["Academic_Risk_Level"] == risk_tier]
        df_sub = df_sub.sort_values(by="Final_Score")

        for _, row in df_sub.iterrows():
            vals = (
                row["Student_ID"],
                row["Student_Name"],
                row["Section"],
                f"{row['Previous_CGPA']:.2f}",
                f"{row['Attendance_Percentage']:.1f}%",
                row["Backlogs"],
                f"{row['Final_Score']:.1f}",
                row["Academic_Risk_Level"]
            )
            self.warn_tree.insert("", tk.END, values=vals)

    # -------------------------------------------------------------------------
    # TAB 4: STUDENT PROFILES
    # -------------------------------------------------------------------------
    def build_profile_tab(self):
        frame = tk.Frame(self.tab_profile, bg=self.LIGHT_BG, padx=20, pady=15)
        frame.pack(fill=tk.BOTH, expand=True)

        search_box = tk.Frame(frame, bg=self.LIGHT_BG)
        search_box.pack(anchor="w", pady=(0, 15))

        tk.Label(search_box, text="Search by Student ID (e.g., SNP005):", font=("Segoe UI", 10, "bold"), bg=self.LIGHT_BG).pack(side=tk.LEFT, padx=(0, 8))
        self.search_ent = tk.Entry(search_box, font=("Segoe UI", 10), width=18)
        self.search_ent.insert(0, "SNP001")
        self.search_ent.pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(search_box, text="🔍 Search Profile", font=("Segoe UI", 9, "bold"), bg=self.NAVY, fg="white", padx=12, command=self.on_search_profile).pack(side=tk.LEFT)

        # Profile Card
        self.card_frame = tk.LabelFrame(frame, text="Student Academic Card", font=("Segoe UI", 10, "bold"), bg="white", padx=20, pady=15)
        self.card_frame.pack(fill=tk.BOTH, expand=True)

        self.prof_name_lbl = tk.Label(self.card_frame, text="Name: --", font=("Segoe UI", 13, "bold"), fg=self.NAVY, bg="white")
        self.prof_name_lbl.pack(anchor="w")

        self.prof_meta_lbl = tk.Label(self.card_frame, text="ID: -- | Section: -- | Gender: --", font=("Segoe UI", 10), fg="#64748B", bg="white")
        self.prof_meta_lbl.pack(anchor="w", pady=(0, 10))

        self.prof_stats_lbl = tk.Label(self.card_frame, text="CGPA: -- | Attendance: -- | Study Hours: -- | Backlogs: --", font=("Segoe UI", 10, "bold"), fg=self.DARK_NAVY, bg="white")
        self.prof_stats_lbl.pack(anchor="w", pady=2)

        self.prof_pred_lbl = tk.Label(self.card_frame, text="Predicted Final Score: -- | Tier: -- | Risk: --", font=("Segoe UI", 10, "bold"), fg="#16A34A", bg="white")
        self.prof_pred_lbl.pack(anchor="w", pady=4)

        # Marks summary text
        tk.Label(self.card_frame, text="Marks Across Six 5th Semester Subjects:", font=("Segoe UI", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 4))
        self.prof_marks_txt = tk.Text(self.card_frame, height=7, width=80, font=("Consolas", 10), relief="solid", bd=1)
        self.prof_marks_txt.pack(anchor="w", fill=tk.X)

        self.on_search_profile()

    def on_search_profile(self):
        query = self.search_ent.get().strip().upper()
        if self.df.empty:
            return

        res = self.df[self.df["Student_ID"] == query]
        if res.empty:
            messagebox.showwarning("Not Found", f"Student ID '{query}' not found. Try SNP001 to SNP300.")
            return

        row = res.iloc[0]
        self.prof_name_lbl.config(text=f"🎓 {row['Student_Name']}")
        self.prof_meta_lbl.config(text=f"Student ID: {row['Student_ID']}  |  {row['Department']}  |  {row['Section']}  |  Age: {row['Age']}")
        self.prof_stats_lbl.config(text=f"CGPA: {row['Previous_CGPA']:.2f} / 10.0   |   Attendance: {row['Attendance_Percentage']:.1f}%   |   Daily Study: {row['Daily_Study_Hours']}h   |   Backlogs: {row['Backlogs']}")
        self.prof_pred_lbl.config(text=f"Predicted Final Score: {row['Final_Score']:.2f} / 100   |   Tier: {row['Predicted_Performance_Category']}   |   Status: {row['Academic_Risk_Level']}")

        self.prof_marks_txt.config(state=tk.NORMAL)
        self.prof_marks_txt.delete(1.0, tk.END)
        self.prof_marks_txt.insert(tk.END, f"  Mathematics (Advanced Engineering Math) : {row['Marks_Mathematics']} / 100\n")
        self.prof_marks_txt.insert(tk.END, f"  Data Structures and Algorithms          : {row['Marks_DSA']} / 100\n")
        self.prof_marks_txt.insert(tk.END, f"  Database Management Systems             : {row['Marks_DBMS']} / 100\n")
        self.prof_marks_txt.insert(tk.END, f"  Operating Systems                       : {row['Marks_OS']} / 100\n")
        self.prof_marks_txt.insert(tk.END, f"  Computer Networks                       : {row['Marks_CN']} / 100\n")
        self.prof_marks_txt.insert(tk.END, f"  Data Mining and Data Wrangling          : {row['Marks_DMW']} / 100\n")
        self.prof_marks_txt.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = EduPredictDesktopApp()
    app.mainloop()
