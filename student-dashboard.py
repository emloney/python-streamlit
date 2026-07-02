"""
Student Performance Analytics Dashboard
----------------------------------------
A Streamlit application that analyzes student performance data
and presents insights through interactive visualizations.

Run locally with:
    streamlit run student-dashboard.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------
# CUSTOM STYLING (HTML / CSS)
# -----------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Overall app background */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Title banner */
    .main-title {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    .main-title h1 {
        font-size: 2.3rem;
        margin-bottom: 5px;
    }
    .main-title p {
        font-size: 1.05rem;
        color: #dfe6f0;
        margin: 0;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    /* Section headers */
    .section-header {
        border-left: 5px solid #4b6cb7;
        padding-left: 12px;
        padding-top: 6px;
        padding-bottom: 6px;
        margin-top: 25px;
        margin-bottom: 10px;
        background-color: #eef1f7;
        border-radius: 4px;
        color: #182848 !important;
    }
    .section-header * {
        color: #182848 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #182848;
    }
    section[data-testid="stSidebar"] * {
        color: #f5f7fa !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# TITLE & DESCRIPTION
# -----------------------------------------------------------------
st.markdown(
    """
    <div class="main-title">
        <h1>🎓 Student Performance Analytics Dashboard</h1>
        <p>Explore, filter, and visualize student academic performance and attendance data
        to uncover trends across departments and semesters.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

try:
    df = load_data("student_performance.csv")
except FileNotFoundError:
    st.error(
        "⚠️ 'student_performance.csv' not found. Please place the file in the "
        "same directory as this script."
    )
    st.stop()

# -----------------------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------------------
st.sidebar.header("🔍 Filters")

departments = sorted(df["Department"].unique())
selected_departments = st.sidebar.multiselect(
    "Department", options=departments, default=departments
)

semesters = sorted(df["Semester"].unique())
selected_semesters = st.sidebar.multiselect(
    "Semester", options=semesters, default=semesters
)

min_att, max_att = int(df["Attendance"].min()), int(df["Attendance"].max())
attendance_range = st.sidebar.slider(
    "Attendance Range (%)",
    min_value=min_att,
    max_value=max_att,
    value=(min_att, max_att),
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ using Streamlit")

# -----------------------------------------------------------------
# APPLY FILTERS
# -----------------------------------------------------------------
filtered_df = df[
    (df["Department"].isin(selected_departments))
    & (df["Semester"].isin(selected_semesters))
    & (df["Attendance"].between(attendance_range[0], attendance_range[1]))
]

if filtered_df.empty:
    st.warning("No records match the selected filters. Please adjust your filter criteria.")
    st.stop()

# -----------------------------------------------------------------
# KEY METRICS
# -----------------------------------------------------------------
st.markdown('<h3 class="section-header">📌 Key Metrics</h3>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", len(filtered_df))
col2.metric("Average Marks", f"{filtered_df['Marks'].mean():.1f}")
col3.metric("Average Attendance", f"{filtered_df['Attendance'].mean():.1f}%")
col4.metric("Top Score", f"{filtered_df['Marks'].max()}")

# -----------------------------------------------------------------
# FILTERED DATA TABLE
# -----------------------------------------------------------------
st.markdown('<h3 class="section-header">📋 Filtered Student Records</h3>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True)

# Download button
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_student_performance.csv",
    mime="text/csv",
)

# -----------------------------------------------------------------
# SUMMARY STATISTICS
# -----------------------------------------------------------------
st.markdown('<h3 class="section-header">📊 Summary Statistics</h3>', unsafe_allow_html=True)
st.dataframe(filtered_df[["Marks", "Attendance"]].describe().T, use_container_width=True)

# -----------------------------------------------------------------
# VISUALIZATIONS
# -----------------------------------------------------------------
st.markdown('<h3 class="section-header">📈 Visual Insights</h3>', unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2)

# Bar chart: average marks by department
with row1_col1:
    st.subheader("Average Marks by Department")
    dept_avg = filtered_df.groupby("Department")["Marks"].mean().sort_values(ascending=False)
    fig1, ax1 = plt.subplots()
    ax1.bar(dept_avg.index, dept_avg.values, color="#4b6cb7")
    ax1.set_xlabel("Department")
    ax1.set_ylabel("Average Marks")
    ax1.set_ylim(0, 100)
    for i, v in enumerate(dept_avg.values):
        ax1.text(i, v + 1, f"{v:.1f}", ha="center")
    st.pyplot(fig1)

# Pie chart: semester distribution
with row1_col2:
    st.subheader("Semester Distribution")
    sem_counts = filtered_df["Semester"].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.pie(
        sem_counts.values,
        labels=[f"Sem {s}" for s in sem_counts.index],
        autopct="%1.1f%%",
        startangle=90,
        colors=plt.cm.Blues_r(range(50, 250, int(200 / max(len(sem_counts), 1)))),
    )
    ax2.axis("equal")
    st.pyplot(fig2)

row2_col1, row2_col2 = st.columns(2)

# Histogram: marks distribution
with row2_col1:
    st.subheader("Marks Distribution")
    fig3, ax3 = plt.subplots()
    ax3.hist(filtered_df["Marks"], bins=10, color="#182848", edgecolor="white")
    ax3.set_xlabel("Marks")
    ax3.set_ylabel("Number of Students")
    st.pyplot(fig3)

# Scatter plot: Attendance vs Marks
with row2_col2:
    st.subheader("Attendance vs Marks")
    fig4, ax4 = plt.subplots()
    scatter = ax4.scatter(
        filtered_df["Attendance"],
        filtered_df["Marks"],
        c=filtered_df["Marks"],
        cmap="viridis",
        alpha=0.8,
    )
    ax4.set_xlabel("Attendance (%)")
    ax4.set_ylabel("Marks")
    fig4.colorbar(scatter, ax=ax4, label="Marks")
    st.pyplot(fig4)

# -----------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------
st.markdown(
    """
    <hr>
    <p style="text-align:center; color:gray; font-size:0.85rem;">
        Student Performance Analytics Dashboard • Built with Streamlit & Pandas
    </p>
    """,
    unsafe_allow_html=True,
)
