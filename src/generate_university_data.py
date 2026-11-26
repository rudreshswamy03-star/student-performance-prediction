"""
Module: generate_university_data.py
Purpose: Synthesize a realistic 300-student engineering cohort dataset for
         Sapthagiri NPS University, Bengaluru (Department of Computer Science and Engineering).
Course: Data Mining and Data Wrangling (5th Semester, 2026-2027)
"""

import os
import random
import numpy as np
import pandas as pd

def generate_university_cohort(n_students: int = 300, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic synthetic dataset for 300 undergraduate engineering students
    studying in their 5th Semester at Sapthagiri NPS University, Bengaluru.
    """
    np.random.seed(random_seed)
    random.seed(random_seed)

    first_names_male = [
        "Aarav", "Rohan", "Vikram", "Karthik", "Aditya", "Rahul", "Nikhil", "Pranav",
        "Siddharth", "Varun", "Tejas", "Chirag", "Gautam", "Darshan", "Manoj",
        "Abhishek", "Harish", "Sanjay", "Chetan", "Vishal", "Akash", "Praveen", "Rakesh"
    ]
    first_names_female = [
        "Ananya", "Sneha", "Pooja", "Priya", "Tanvi", "Divya", "Kavya", "Deepa",
        "Meghana", "Shruti", "Bhavana", "Swati", "Rashmi", "Keerthi", "Nandini",
        "Aishwarya", "Monika", "Rakshita", "Sahana", "Shreya", "Neha", "Spoorthi"
    ]
    last_names = [
        "Sharma", "Rao", "Patil", "Kulkarni", "Murthy", "Hegde", "Nair", "Swamy",
        "Gowda", "Desai", "Bhat", "Reddy", "Kumar", "Prasad", "Shetty", "Joshi",
        "Kamath", "Verma", "Shastry", "Naik", "Acharya", "Iyengar", "Mishra"
    ]

    records = []

    for i in range(1, n_students + 1):
        student_id = f"SNP{i:03d}"
        gender = "Male" if random.random() < 0.54 else "Female"
        if gender == "Male":
            name = f"{random.choice(first_names_male)} {random.choice(last_names)}"
        else:
            name = f"{random.choice(first_names_female)} {random.choice(last_names)}"

        dept = "Computer Science and Engineering"
        academic_year = "2026–2027"
        semester = "5th Semester"
        section = random.choice(["Section A", "Section B", "Section C"])
        age = int(np.random.choice([19, 20, 21, 22], p=[0.10, 0.65, 0.20, 0.05]))

        # Underlying academic capability baseline factor (latent variable ~ N(0, 1))
        latent_ability = np.random.normal(0, 1)

        # Previous Semester CGPA (scale: 4.0 - 10.0)
        base_cgpa = 7.2 + 1.1 * latent_ability + np.random.normal(0, 0.4)
        cgpa = float(np.clip(round(base_cgpa, 2), 4.20, 9.85))

        # Backlogs (correlated negatively with CGPA)
        if cgpa >= 8.5:
            backlogs = int(np.random.choice([0, 1], p=[0.95, 0.05]))
        elif cgpa >= 7.0:
            backlogs = int(np.random.choice([0, 1, 2], p=[0.80, 0.16, 0.04]))
        elif cgpa >= 5.5:
            backlogs = int(np.random.choice([0, 1, 2, 3], p=[0.45, 0.35, 0.15, 0.05]))
        else:
            backlogs = int(np.random.choice([1, 2, 3, 4], p=[0.25, 0.40, 0.25, 0.10]))

        # Attendance Percentage (scale: 40% - 99%)
        base_attendance = 78 + 8 * latent_ability - (2.5 * backlogs) + np.random.normal(0, 6)
        attendance = float(np.clip(round(base_attendance, 1), 45.0, 98.5))
        absence_days = int(round((100.0 - attendance) * 0.45))

        # Study Habits
        study_hours = float(np.clip(round(2.5 + 0.9 * latent_ability + (0.03 * attendance) + np.random.normal(0, 0.7), 1), 1.0, 8.0))
        library_hours = float(np.clip(round(3.0 + 1.2 * latent_ability + np.random.normal(0, 2.0), 1), 0.0, 14.0))
        online_learning_hours = float(np.clip(round(4.0 + np.random.normal(0, 2.5), 1), 1.0, 15.0))
        assignment_completion = float(np.clip(round(75 + 10 * latent_ability + (0.15 * attendance) + np.random.normal(0, 7), 1), 42.0, 100.0))
        extracurricular = "Yes" if random.random() < 0.48 else "No"

        # Previous Semester Standing label
        if cgpa >= 8.5:
            prev_standing = "Distinction"
        elif cgpa >= 7.0:
            prev_standing = "First Class"
        elif cgpa >= 5.5:
            prev_standing = "Second Class"
        elif cgpa >= 4.5:
            prev_standing = "Pass Class"
        else:
            prev_standing = "At Risk"

        # Six Core 5th Semester Subjects (Marks scale: 0 - 100)
        # Expected mark depends on latent ability, study hours, and subject difficulty
        def generate_subject_mark(difficulty_offset: float = 0.0):
            mark = 65 + (8.5 * latent_ability) + (1.8 * study_hours) + (0.12 * attendance) - (3.0 * backlogs) + difficulty_offset + np.random.normal(0, 6.5)
            return float(np.clip(round(mark, 1), 22.0, 99.0))

        marks_math = generate_subject_mark(difficulty_offset=-3.5)       # Math has higher difficulty
        marks_dsa = generate_subject_mark(difficulty_offset=-2.0)        # DSA is moderately challenging
        marks_dbms = generate_subject_mark(difficulty_offset=2.5)        # DBMS has higher average
        marks_os = generate_subject_mark(difficulty_offset=-1.0)          # OS is standard
        marks_cn = generate_subject_mark(difficulty_offset=0.5)           # Computer Networks
        marks_dmw = generate_subject_mark(difficulty_offset=1.5)          # Data Mining & Data Wrangling

        subject_avg = (marks_math + marks_dsa + marks_dbms + marks_os + marks_cn + marks_dmw) / 6.0
        internal_assessment = float(round(subject_avg * 0.95 + np.random.normal(0, 2.5), 1))
        internal_assessment = float(np.clip(internal_assessment, 25.0, 98.0))

        # Target Variable Formulation: Final Semester Performance Score (0 - 100)
        # Combined weighted formula with realistic variance & unexpected variations
        final_score_raw = (
            (0.40 * subject_avg) +
            (0.25 * (cgpa * 10.0)) +
            (0.12 * attendance) +
            (0.10 * assignment_completion) +
            (0.08 * (study_hours * 10.0)) +
            (0.05 * (internal_assessment)) -
            (2.2 * backlogs) +
            np.random.normal(0, 3.2) # Realistic student variance
        )
        final_score = float(np.clip(round(final_score_raw, 2), 25.0, 99.5))

        # Target Performance Classification Category
        if final_score >= 85.0:
            performance_category = "Excellent"
            risk_level = "Low Risk"
        elif final_score >= 70.0:
            performance_category = "Very Good"
            risk_level = "Low Risk"
        elif final_score >= 60.0:
            performance_category = "Good"
            risk_level = "Low Risk"
        elif final_score >= 50.0:
            performance_category = "Average"
            risk_level = "Medium Risk"
        else:
            performance_category = "Needs Improvement"
            risk_level = "High Risk"

        records.append({
            "Student_ID": student_id,
            "Student_Name": name,
            "Department": dept,
            "Academic_Year": academic_year,
            "Current_Semester": semester,
            "Section": section,
            "Gender": gender,
            "Age": age,
            "Previous_CGPA": cgpa,
            "Attendance_Percentage": attendance,
            "Absence_Days": absence_days,
            "Daily_Study_Hours": study_hours,
            "Weekly_Library_Hours": library_hours,
            "Online_Learning_Hours": online_learning_hours,
            "Assignment_Completion_Percentage": assignment_completion,
            "Internal_Assessment_Marks": internal_assessment,
            "Previous_Semester_Performance": prev_standing,
            "Backlogs": backlogs,
            "Extracurricular_Participation": extracurricular,
            "Marks_Mathematics": marks_math,
            "Marks_DSA": marks_dsa,
            "Marks_DBMS": marks_dbms,
            "Marks_OS": marks_os,
            "Marks_CN": marks_cn,
            "Marks_DMW": marks_dmw,
            "Final_Score": final_score,
            "Predicted_Performance_Category": performance_category,
            "Academic_Risk_Level": risk_level
        })

    df = pd.DataFrame(records)
    return df

def save_university_dataset(output_path: str = "dataset/university_students.csv") -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = generate_university_cohort(n_students=300, random_seed=42)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] University student cohort generated: {len(df)} records saved to '{output_path}'.")
    return output_path

if __name__ == "__main__":
    path = save_university_dataset()
    df = pd.read_csv(path)
    print("Dataset Shape:", df.shape)
    print("\nSample Records:")
    print(df[["Student_ID", "Student_Name", "Section", "Previous_CGPA", "Attendance_Percentage", "Final_Score", "Predicted_Performance_Category"]].head())
    print("\nPerformance Category Distribution:")
    print(df["Predicted_Performance_Category"].value_counts())
    print("\nAcademic Risk Distribution:")
    print(df["Academic_Risk_Level"].value_counts())
