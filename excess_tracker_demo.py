import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sample report data
report_data = [
    {"Report ID": "R001", "Department": "Finance", "Stage": "Stage 1", "Last Updated": datetime.now() - timedelta(hours=5)},
    {"Report ID": "R002", "Department": "HR", "Stage": "Stage 2", "Last Updated": datetime.now() - timedelta(hours=26)},
    {"Report ID": "R003", "Department": "IT", "Stage": "Stage 3", "Last Updated": datetime.now() - timedelta(hours=10)},
    {"Report ID": "R004", "Department": "Finance", "Stage": "Stage 4", "Last Updated": datetime.now() - timedelta(hours=30)},
]

# Convert to DataFrame
df = pd.DataFrame(report_data)

# Title
st.title("Excess Report Tracker Demo")

# Function to advance stage
def advance_stage(stage):
    stages = ["Stage 1", "Stage 2", "Stage 3", "Stage 4"]
    if stage in stages and stage != "Stage 4":
        return stages[stages.index(stage) + 1]
    return stage

# Update stage buttons
st.subheader("Report Clearance Table")
for i, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])
    col1.write(row["Report ID"])
    col2.write(row["Department"])
    col3.write(row["Stage"])
    col4.write(row["Last Updated"].strftime("%Y-%m-%d %H:%M"))
    overdue = datetime.now() - row["Last Updated"] > timedelta(hours=24)
    if overdue:
        col5.markdown("⚠️ Overdue")
    else:
        if col5.button(f"Advance {row['Report ID']}", key=row["Report ID"]):
            df.at[i, "Stage"] = advance_stage(row["Stage"])
            df.at[i, "Last Updated"] = datetime.now()

# Departmental Summary
st.subheader("Departmental Summary")
summary = df.groupby(["Department", "Stage"]).size().unstack(fill_value=0)
st.dataframe(summary)

# Overdue Reports
st.subheader("Overdue Reports")
overdue_df = df[df["Last Updated"] < datetime.now() - timedelta(hours=24)]
st.dataframe(overdue_df)
