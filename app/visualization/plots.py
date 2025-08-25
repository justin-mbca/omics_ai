import pandas as pd
import plotly.express as px
import streamlit as st

def plot_scatter(df: pd.DataFrame, x: str, y: str):
    fig = px.scatter(df, x=x, y=y)
    st.plotly_chart(fig)

def plot_heatmap(df: pd.DataFrame):
    fig = px.imshow(df.corr())
    st.plotly_chart(fig)
