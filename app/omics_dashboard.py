import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from analysis.data_summary import summarize_data
from visualization.plots import plot_scatter, plot_heatmap
from ml.clustering import run_kmeans


st.title("Omics Dashboard (Modularized)")

tab1, tab2 = st.tabs(["Update Data & Analysis", "Demo"])

with tab1:
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

with tab2:
    st.write("Demo: Example analysis with synthetic omics data.")
    import numpy as np
    np.random.seed(42)
    samples = [f"Sample_{i}" for i in range(1, 21)]
    genes = [f"Gene_{i}" for i in range(1, 101)]
    expression_data = np.random.lognormal(mean=2, sigma=1.5, size=(20, 100))
    expression_df = pd.DataFrame(expression_data, index=samples, columns=genes)

    st.write("Data Preview:")
    st.dataframe(expression_df.head())
    st.write("Summary Statistics:")
    st.dataframe(summarize_data(expression_df))

    st.write("Scatter Plot:")
    x_col = st.selectbox("Demo X Axis", expression_df.columns, index=0, key="demo_x")
    y_col = st.selectbox("Demo Y Axis", expression_df.columns, index=1, key="demo_y")
    plot_scatter(expression_df, x_col, y_col)

    st.write("Heatmap (Correlation):")
    plot_heatmap(expression_df)

    st.write("KMeans Clustering:")
    n_clusters = st.slider("Demo Number of clusters", 2, 10, 3, key="demo_clusters")
    labels = run_kmeans(expression_df, n_clusters)
    st.write("Cluster Labels:")
    st.write(labels)
