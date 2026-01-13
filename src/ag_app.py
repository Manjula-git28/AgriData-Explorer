import streamlit as st
import pandas as pd
import plotly.express as px
from db import get_connection
from queries import queries

st.set_page_config(page_title="AgriData Explorer", layout="wide")

st.title("🌾 AgriData Explorer")
st.markdown("Indian Agriculture Analytics Platform")

option = st.sidebar.selectbox(
    "Choose Analysis",
    list(queries.keys())
)

conn = get_connection()
df = pd.read_sql(queries[option], conn)

st.subheader(option)
st.dataframe(df)

if option == "Rice Trend Top 3":
    fig = px.line(df, x="year", y="rice_production", color="state_name")
    st.plotly_chart(fig, use_container_width=True)

elif option == "Wheat Yield Growth":
    fig = px.bar(df, x="increase", y="dist_name", orientation="h")
    st.plotly_chart(fig, use_container_width=True)
