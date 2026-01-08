import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuration ---
st.set_page_config(layout="wide", page_title="Data Quality Microservice")
APP_TITLE = "Fullbooker Pipeline Optimization: Conversion Drivers Analysis"

# Load the clean features data created by the ETL script
try:
    df = pd.read_csv('02_clean_features.csv')
    df['is_converted'] = df['is_converted'].astype(bool)
    df['Conversion Status'] = np.where(df['is_converted'], 'Booked', 'Not Booked')
except FileNotFoundError:
    st.error("Data file '02_clean_features.csv' not found. Please run data_pipeline.py first.")
    st.stop()

# --- Dashboard Layout ---
st.title(APP_TITLE)
st.caption("Demonstrating ETL, Feature Engineering, and Production-Ready Visualization.")
st.markdown("---")

# 1. KPI Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Analyzed Users", df['user_id'].nunique())
col2.metric("Overall Conversion Rate", f"{df['is_converted'].mean() * 100:.2f}%")
col3.metric("Avg. Recency (Days)", f"{df['recency_days'].mean():.1f}")

st.markdown("---")

# 2. Feature Analysis: Recency vs. Views
st.header("Feature 1: Recency vs. Total Views")
fig1 = px.scatter(
    df, x='recency_days', y='total_views',
    color='Conversion Status',
    hover_data=['avg_price_viewed'],
    title='Recency (Days Since Last Interaction) vs. Total Views',
    height=500,
    color_discrete_map={'Booked': '#10b981', 'Not Booked': '#ef4444'}
)
st.plotly_chart(fig1, use_container_width=True)

# 3. Feature Analysis: Price Drivers
st.header("Feature 2: Price Impact on Conversion")
fig2 = px.box(
    df, x='Conversion Status', y='avg_price_viewed',
    color='Conversion Status',
    title='Distribution of Average Viewed Price by Conversion Status',
    color_discrete_map={'Booked': '#10b981', 'Not Booked': '#ef4444'}
)
st.plotly_chart(fig2, use_container_width=True)