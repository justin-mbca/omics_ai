import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from analysis.data_summary import summarize_data
from analysis.pca_quality import show_quality_metrics, show_pca
from visualization.plots import plot_scatter, plot_heatmap
from ml.clustering import run_kmeans
from ml.classification import run_classification
from ml.feature_selection import select_top_features
from demo_tab import render_demo_tab


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

        # Quality Metrics
        show_quality_metrics(df)

        # PCA Analysis
        show_pca(df)

        st.write("Scatter Plot:")
        if len(df.columns) >= 2:
            x_col = st.selectbox("X Axis", df.columns, index=0)
            y_col = st.selectbox("Y Axis", df.columns, index=1)
            plot_scatter(df, x_col, y_col)

        st.write("Heatmap (Correlation):")
        if df is not None and df.select_dtypes(include="number").shape[1] >= 2:
            plot_heatmap(df, key="user_heatmap")
        else:
            st.info("Not enough numeric columns for heatmap.")


        # KMeans Clustering
        if df is not None and df.select_dtypes(include="number").shape[1] >= 2:
            st.write("KMeans Clustering:")
            n_clusters = st.slider("Number of clusters", 2, 10, 3)
            labels = run_kmeans(df, n_clusters)
            st.write("Cluster Labels:")
            st.write(labels)
        else:
            st.info("Not enough numeric columns for clustering.")

        # Classification
        st.write("Classification (Supervised Learning):")
        label_options = [col for col in df.columns if df[col].nunique() <= 10 and df[col].dtype in ["object", "category", "int64"]]
        if label_options:
            label_col = st.selectbox("Select label column for classification", label_options)
            run_classification(df, label_col)
        else:
            st.info("No suitable label column found for classification (should be categorical with <=10 unique values).")

        # Feature Selection
        st.write("Feature Selection:")
        if label_options:
            label_col_fs = st.selectbox("Select label column for feature selection", label_options, key="fs_label")
            k = st.slider("Number of top features to select", 2, min(20, df.select_dtypes(include='number').shape[1]), 5)
            select_top_features(df, label_col_fs, k)
        else:
            st.info("No suitable label column found for feature selection.")

with tab2:
    render_demo_tab()
