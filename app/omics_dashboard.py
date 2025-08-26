import streamlit as st
from utils.data_loader import load_data
from analysis.data_summary import summarize_data
from analysis.pca_quality import show_quality_metrics, show_pca
from visualization.plots import plot_scatter, plot_heatmap
from ml.clustering import run_kmeans
from ml.classification import run_classification
from ml.feature_selection import select_top_features
from demo_tab import render_demo_tab


st.set_page_config(page_title="Omics Dashboard", layout="wide")
st.title("Omics Dashboard (Modularized)")

# Sidebar: global settings and example data download
with st.sidebar:
    st.header("Settings & Resources")
    st.markdown("Download an example omics dataset:")
    with open("data/example_omics.csv", "rb") as f:
        st.download_button("Download Example CSV", f, file_name="example_omics.csv")
    st.markdown("---")
    st.info("You can upload your own CSV or use the example above.")
    st.markdown("---")
    st.markdown("**Theme:** (future option)")
    st.markdown("**API Key:** (future option)")

tab1, tab2, tab3 = st.tabs(["Update Data & Analysis", "Demo", "AI Assistant (LLM Demo)"])

with tab1:
    st.write("Upload a public or anonymized omics dataset to explore analysis, visualization, and ML features.")
    uploaded_file = st.file_uploader("Upload your omics data (CSV)")
    df = load_data(uploaded_file)
    if df is not None:
        st.write("Data Preview:")
        st.caption("Preview of the first few rows of your data.")
        st.dataframe(df.head())
        st.write("Summary Statistics:")
        st.dataframe(summarize_data(df))
        st.caption("Descriptive statistics for all columns.")

        # Quality Control
        st.markdown("### Quality Control")
        st.help("View summary statistics and feature correlations. Outlier detection coming soon.")
        show_quality_metrics(df)

        # PCA Analysis
        st.markdown("### PCA Analysis")
        st.help("Principal Component Analysis (PCA) visualizes sample clustering and variance structure.")
        show_pca(df)

        # Scatter Plot
        st.markdown("### Scatter Plot")
        st.help("Select two features to plot against each other.")
        if len(df.columns) >= 2:
            x_col = st.selectbox("X Axis", df.columns, index=0)
            y_col = st.selectbox("Y Axis", df.columns, index=1)
            plot_scatter(df, x_col, y_col)

        # Heatmap
        st.markdown("### Heatmap (Correlation)")
        st.help("Visualize correlations between numeric features.")
        if df is not None and df.select_dtypes(include="number").shape[1] >= 2:
            plot_heatmap(df, key="user_heatmap")
        else:
            st.info("Not enough numeric columns for heatmap.")

        # KMeans Clustering
        st.markdown("### KMeans Clustering")
        st.help("Group samples into clusters based on feature similarity.")
        if df is not None and df.select_dtypes(include="number").shape[1] >= 2:
            n_clusters = st.slider("Number of clusters", 2, 10, 3)
            labels = run_kmeans(df, n_clusters)
            st.write("Cluster Labels:")
            st.write(labels)
        else:
            st.info("Not enough numeric columns for clustering.")

        # Classification
        st.markdown("### Classification (Supervised Learning)")
        st.help("Predict sample classes using Random Forest. Select a label column with <=10 unique values.")
        label_options = [col for col in df.columns if df[col].nunique() <= 10 and df[col].dtype in ["object", "category", "int64"]]
        if label_options:
            label_col = st.selectbox("Select label column for classification", label_options)
            run_classification(df, label_col)
        else:
            st.info("No suitable label column found for classification (should be categorical with <=10 unique values).")

        # Feature Selection
        st.markdown("### Feature Selection")
        st.help("Identify top features associated with the selected label using ANOVA F-test.")
        if label_options:
            label_col_fs = st.selectbox("Select label column for feature selection", label_options, key="fs_label")
            k = st.slider("Number of top features to select", 2, min(20, df.select_dtypes(include='number').shape[1]), 5)
            select_top_features(df, label_col_fs, k)
        else:
            st.info("No suitable label column found for feature selection.")

        # Normalization (simple option)
        st.markdown("### Data Normalization")
        st.help("Apply z-score normalization to numeric features.")
        if st.button("Normalize Data (z-score)"):
            numeric_cols = df.select_dtypes(include='number').columns
            df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
            st.success("Numeric features normalized (z-score). Continue analysis with normalized data.")

        # Export/Reporting
        st.markdown("### Export & Reporting")
        st.help("Download your results and plots. Automated report generation coming soon.")
        st.download_button("Download Data (CSV)", df.to_csv(index=False).encode(), file_name="omics_results.csv", key="download_csv_main")
        # (Optional) Add plot export and PDF/HTML report in future

        # Export/Reporting
        st.markdown("### Export & Reporting")
        st.help("Download your results and plots. Automated report generation coming soon.")
        st.download_button("Download Data (CSV)", df.to_csv(index=False).encode(), file_name="omics_results.csv", key="download_csv_secondary")
        # (Optional) Add plot export and PDF/HTML report in future


with tab3:
    st.header("AI Assistant (LLM Demo)")
    st.info("This is a demo of LLM-powered features. Connect an API key for real AI responses.")

    st.subheader("1. Natural Language Summary")
    if st.button("Generate Summary (Demo)", key="llm_summary"):
        st.success("""
**Summary:**\nThis dataset contains N samples and M features. Main clusters and patterns have been visualized. For a full summary, connect an LLM API.
        """)

    st.subheader("2. Q&A / Chatbot")
    user_question = st.text_input("Ask a question about your data or results (Demo)", key="llm_qa")
    if user_question:
        st.info(f"LLM Answer: This is a demo response. Connect an LLM API for real answers to: '{user_question}'")

    st.subheader("3. Automated Report Generation")
    if st.button("Generate Report (Demo)", key="llm_report"):
        st.success("""
**Report:**\nThis is a demo report generated by an LLM. It would include data summary, analysis steps, results, and interpretations. Connect an LLM API for real reports.
        """)

    st.subheader("4. Data Interpretation")
    if st.button("Suggest Biological Interpretation (Demo)", key="llm_interpret"):
        st.info("LLM Suggestion: This is a demo biological interpretation. Connect an LLM API for real insights.")

    st.subheader("5. Code Generation / Assistance")
    code_request = st.text_input("Describe the analysis code you want (Demo)", key="llm_code")
    if code_request:
        st.code("# Demo code snippet. Connect an LLM API for real code generation.\nimport pandas as pd\n# ...")

    st.subheader("6. Interactive Tutorials / Help")
    if st.button("Show Help (Demo)", key="llm_help"):
        st.info("LLM Help: This is a demo help message. Connect an LLM API for real interactive help.")

    st.subheader("7. Data Cleaning Suggestions")
    if st.button("Suggest Data Cleaning (Demo)", key="llm_clean"):
        st.info("LLM Suggestion: This is a demo data cleaning suggestion. Connect an LLM API for real recommendations.")

with tab2:
    render_demo_tab()
