# Student Performance Analytics Dashboard

A Streamlit web app that analyzes student performance data (marks, attendance,
department, semester) and presents interactive visualizations.

## Files

| File | Purpose |
|---|---|
| `student-dashboard.py` | Main Streamlit application |
| `student_performance.csv` | Sample dataset (60 student records) |
| `requirements.txt` | Python dependencies |

## Features

- Title banner + description with custom CSS styling
- Sidebar filters: Department, Semester, Attendance range
- Filtered data table + CSV download button
- Summary statistics (describe table for Marks & Attendance)
- Visualizations:
  - Bar chart — average marks by department
  - Pie chart — semester distribution
  - Histogram — marks distribution
  - Scatter plot — attendance vs marks

---

## 1. Run Locally

```bash
# 1. Create a project folder and put these 3 files inside it:
#    student-dashboard.py, student_performance.csv, requirements.txt

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run student-dashboard.py
```

The app opens automatically at `http://localhost:8501`.

---

## 2. Deploy to Streamlit Community Cloud (free, public URL)

### Step A — Push the project to GitHub

1. Create a new **public** GitHub repository, e.g. `student-performance-dashboard`.
2. Add these files to the repo root:
   - `student-dashboard.py`
   - `student_performance.csv`
   - `requirements.txt`
3. Commit and push:
   ```bash
   git init
   git add .
   git commit -m "Student performance dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/student-performance-dashboard.git
   git push -u origin main
   ```

### Step B — Deploy on Streamlit Community Cloud

1. Go to **https://share.streamlit.io** and sign in with your GitHub account.
2. Click **"Create app"** (or **"New app"**).
3. Choose **"Deploy a public app from GitHub"**.
4. Fill in:
   - **Repository:** `<your-username>/student-performance-dashboard`
   - **Branch:** `main`
   - **Main file path:** `student-dashboard.py`
5. Click **"Deploy"**.
6. Streamlit Cloud will install the packages from `requirements.txt` and build
   the app. This takes 1-2 minutes.
7. Once live, you'll get a public URL in the form:
   ```
   https://<your-app-name>-<random-id>.streamlit.app
   ```
8. Copy and share that URL — anyone can open it, no login required.

### Notes

- Any time you push new commits to the `main` branch, the deployed app
  auto-updates.
- If you update `student_performance.csv` with more records, just replace the
  file in the repo and push — no code changes needed.
- To keep the app awake, Streamlit Cloud free tier apps sleep after a period
  of inactivity; opening the URL wakes them back up (may take ~30 seconds).

---

## Sample Data Schema

| Column | Type | Description |
|---|---|---|
| Student_ID | int | Unique student identifier |
| Name | string | Student name |
| Department | string | BCA / BSc / BCom / BBA |
| Semester | int | 1–6 |
| Marks | int | 0–100 |
| Attendance | int | Attendance percentage (0–100) |
