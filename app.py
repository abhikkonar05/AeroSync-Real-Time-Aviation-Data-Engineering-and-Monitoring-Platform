import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
from database.connection import engine
from monitoring.pipeline_health import get_pipeline_logs

st.title("✈ AeroSync Aviation Dashboard")

df = pd.read_sql("SELECT * FROM flights", engine)

st.subheader("Flight Data")
st.dataframe(df)

st.subheader("Delay Distribution")
st.bar_chart(df["delay_minutes"])

st.subheader("Pipeline Logs")
logs = get_pipeline_logs()
st.dataframe(logs)