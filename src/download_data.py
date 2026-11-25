"""
Module: download_data.py
Purpose: Automatically fetch and extract the UCI Student Performance Dataset.
Course: Data Mining and Data Wrangling
"""

import os
import io
import urllib.request
import zipfile

def download_and_extract_dataset(target_dir: str = "dataset") -> None:
    """
    Downloads student+performance.zip from the official UCI Machine Learning Repository
    and extracts the Mathematics course dataset (student-mat.csv) and metadata.
    """
    os.makedirs(target_dir, exist_ok=True)
    dataset_url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
    
    print(f"[INFO] Connecting to UCI Repository: {dataset_url}")
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(dataset_url, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        outer_zip_bytes = response.read()
        print("[INFO] Successfully downloaded outer archive.")
        
        with zipfile.ZipFile(io.BytesIO(outer_zip_bytes)) as outer_zip:
            # The archive contains an inner student.zip
            with zipfile.ZipFile(io.BytesIO(outer_zip.read("student.zip"))) as inner_zip:
                files_to_extract = ["student-mat.csv", "student-por.csv", "student.txt"]
                for filename in files_to_extract:
                    inner_zip.extract(filename, path=target_dir)
                    print(f"[INFO] Extracted '{filename}' to '{target_dir}/'")

    print("[SUCCESS] Dataset download and extraction completed successfully.")

if __name__ == "__main__":
    download_and_extract_dataset()
