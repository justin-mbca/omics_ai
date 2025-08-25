import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from analysis.data_summary import summarize_data
from visualization.plots import plot_scatter, plot_heatmap
from ml.clustering import run_kmeans

st.title("Omics Dashboard (Modularized)")

st.write("Upload a public or anonymized omics dataset to explore analysis, visualization, and ML features.")

uploaded_file = st.file_uploader("Upload your omics data (CSV)")
df = load_data(uploaded_file)
if df is not None:
    st.write("Data Preview:")
    st.dataframe(df.head())
    st.write("Summary Statistics:")
    st.dataframe(summarize_data(df))

    st.write("Scatter Plot:")
    if len(df.columns) >= 2:
        x_col = st.selectbox("X Axis", df.columns, index=0)
        y_col = st.selectbox("Y Axis", df.columns, index=1)
        plot_scatter(df, x_col, y_col)

    st.write("Heatmap (Correlation):")
    plot_heatmap(df)

    st.write("KMeans Clustering:")
    n_clusters = st.slider("Number of clusters", 2, 10, 3)
    labels = run_kmeans(df, n_clusters)
    st.write("Cluster Labels:")
    st.write(labels)
