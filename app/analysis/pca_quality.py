import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from sklearn.decomposition import PCA

def show_quality_metrics(df: pd.DataFrame):
    st.subheader("Quality Metrics (Basic)")
    st.dataframe(df.describe(include='all'), use_container_width=True)
    st.subheader("Correlation Heatmap")
    if df.select_dtypes(include=np.number).shape[1] > 1:
        fig_corr = px.imshow(df.select_dtypes(include=np.number).corr())
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough numeric columns for correlation heatmap.")

def show_pca(df: pd.DataFrame):
    st.subheader("PCA Analysis")
    numeric_df = df.select_dtypes(include=np.number)
    if numeric_df.shape[1] < 2:
        st.info("Not enough numeric columns for PCA.")
        return
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(numeric_df.fillna(0))
    pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
    pca_df["Sample"] = df.index if df.index.size == pca_df.shape[0] else range(pca_df.shape[0])
    fig_pca = px.scatter(pca_df, x="PC1", y="PC2", hover_data=["Sample"])
    st.plotly_chart(fig_pca, use_container_width=True)
    st.write(f"Explained variance: PC1 = {pca.explained_variance_ratio_[0]:.2%}, PC2 = {pca.explained_variance_ratio_[1]:.2%}")
