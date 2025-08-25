import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64

# Set up the page
st.set_page_config(
    page_title="OmicsAI Dashboard",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1f77b4; padding-bottom: 10px}
    .section-header {font-size: 1.8rem; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding: 10px 0}
    .feature-box {background-color: #f0f7ff; padding: 20px; border-radius: 10px; margin: 10px 0}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🧬 OmicsAI - Multi-Omics Analysis Platform</p>', unsafe_allow_html=True)
st.write("AI-powered integration and visualization of genomics, transcriptomics, and proteomics data")

# Sidebar
with st.sidebar:
    st.header("Data Configuration")
    
    # Data selection
    dataset_option = st.selectbox(
        "Select dataset",
        ["TCGA Breast Cancer", "Single-cell RNA-seq", "Proteomics Atlas", "Upload custom data"]
    )
    
    # Analysis type
    analysis_type = st.multiselect(
        "Analysis types",
        ["Quality Control", "Differential Expression", "Pathway Analysis", "Multi-omics Integration"],
        default=["Quality Control", "Multi-omics Integration"]
    )
    
    # AI model selection
    st.subheader("AI Models")
    use_alphafold = st.checkbox("AlphaFold Protein Structure", value=True)
    use_deepvariant = st.checkbox("DeepVariant Calling", value=True)
    use_mofa = st.checkbox("MOFA+ Integration", value=True)
    
    # Parameters
    st.subheader("Parameters")
    p_value = st.slider("P-value threshold", 0.01, 0.1, 0.05)
    min_expression = st.slider("Minimum expression level", 0.0, 10.0, 1.0)
    
    # Run analysis button
    if st.button("Run Analysis", type="primary"):
        st.session_state.analysis_run = True

# Main content
tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Data Quality", "Integration Analysis", "Protein Structures"])

with tab1:
    st.markdown('<p class="section-header">Overview Dashboard</p>', unsafe_allow_html=True)
    
    # Create some mock data
    np.random.seed(42)
    samples = [f"Sample_{i}" for i in range(1, 21)]
    genes = [f"Gene_{i}" for i in range(1, 101)]
    
    # Generate mock expression data
    expression_data = np.random.lognormal(mean=2, sigma=1.5, size=(20, 100))
    expression_df = pd.DataFrame(expression_data, index=samples, columns=genes)
    
    # Generate mock variant data
    variants = [f"Variant_{i}" for i in range(1, 11)]
    variant_counts = np.random.poisson(lam=3, size=(20, 10))
    variant_df = pd.DataFrame(variant_counts, index=samples, columns=variants)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gene Expression Heatmap")
        fig_heatmap = px.imshow(expression_data, 
                               labels=dict(x="Genes", y="Samples", color="Expression"),
                               x=genes, y=samples)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.subheader("Variant Distribution")
        fig_variant = px.bar(variant_df.sum(), 
                            labels=dict(index="Variant", value="Count", color="Variant"))
        st.plotly_chart(fig_variant, use_container_width=True)
    
    with col2:
        st.subheader("PCA Analysis")
        # Mock PCA data
        pca_data = np.random.normal(size=(20, 2))
        pca_df = pd.DataFrame(pca_data, columns=['PC1', 'PC2'])
        pca_df['Sample'] = samples
        pca_df['Group'] = ['Control' if i < 10 else 'Treatment' for i in range(20)]
        
        fig_pca = px.scatter(pca_df, x='PC1', y='PC2', color='Group', hover_data=['Sample'])
        st.plotly_chart(fig_pca, use_container_width=True)
        
        st.subheader("Expression Distribution")
        fig_dist = px.box(expression_df.iloc[:, :5], 
                         labels=dict(variable="Gene", value="Expression Level"))
        st.plotly_chart(fig_dist, use_container_width=True)

with tab2:
    st.markdown('<p class="section-header">Data Quality Control</p>', unsafe_allow_html=True)
    
    # Mock quality metrics
    qc_metrics = pd.DataFrame({
        'Sample': samples,
        'Reads': np.random.normal(5e6, 1e6, 20),
        'Mapping Rate (%)': np.random.normal(85, 5, 20),
        'Duplication Rate (%)': np.random.normal(15, 5, 20),
        'rRNA Rate (%)': np.random.normal(5, 2, 20)
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quality Metrics")
        st.dataframe(qc_metrics, use_container_width=True)
        
        st.subheader("Mapping Rate Distribution")
        fig_map = px.histogram(qc_metrics, x='Mapping Rate (%)', nbins=10)
        st.plotly_chart(fig_map, use_container_width=True)
    
    with col2:
        st.subheader("Quality Metrics Correlation")
        fig_qc_corr = px.imshow(qc_metrics.select_dtypes(include=np.number).corr())
        st.plotly_chart(fig_qc_corr, use_container_width=True)
        
        st.subheader("Outlier Detection")
        # Mock outlier scores
        outlier_scores = np.random.beta(1, 10, 20)
        outlier_df = pd.DataFrame({'Sample': samples, 'Outlier Score': outlier_scores})
        outlier_df['Outlier'] = outlier_df['Outlier Score'] > 0.7
        
        fig_outlier = px.bar(outlier_df, x='Sample', y='Outlier Score', color='Outlier')
        st.plotly_chart(fig_outlier, use_container_width=True)

with tab3:
    st.markdown('<p class="section-header">Multi-Omics Integration</p>', unsafe_allow_html=True)
    
    # Mock MOFA+ integration results
    factors = 5
    factor_loadings = np.random.normal(size=(100, factors))
    factor_df = pd.DataFrame(factor_loadings, 
                            columns=[f'Factor_{i+1}' for i in range(factors)],
                            index=genes)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Factor Loadings (Top Genes)")
        top_genes = factor_df.abs().max(axis=1).sort_values(ascending=False).index[:10]
        st.dataframe(factor_df.loc[top_genes], use_container_width=True)
        
        st.subheader("Variance Explained per Factor")
        variance = np.random.dirichlet(np.ones(factors)*2, size=1)[0] * 100
        var_df = pd.DataFrame({'Factor': [f'Factor_{i+1}' for i in range(factors)], 
                              'Variance (%)': variance})
        fig_var = px.pie(var_df, names='Factor', values='Variance (%)')
        st.plotly_chart(fig_var, use_container_width=True)
    
    with col2:
        st.subheader("Factor Weights Heatmap")
        fig_factor_heatmap = px.imshow(factor_loadings, 
                                      labels=dict(x="Factor", y="Gene", color="Weight"),
                                      x=[f'Factor_{i+1}' for i in range(factors)], y=genes)
        st.plotly_chart(fig_factor_heatmap, use_container_width=True)
        
        st.subheader("Pathway Enrichment")
        pathways = ['Cell Cycle', 'DNA Repair', 'Metabolism', 'Immune Response', 'Apoptosis']
        enrichment_scores = -np.log10(np.random.uniform(0.001, 0.1, len(pathways)))
        pathway_df = pd.DataFrame({'Pathway': pathways, 'Enrichment Score': enrichment_scores})
        
        fig_pathway = px.bar(pathway_df, x='Enrichment Score', y='Pathway', orientation='h')
        st.plotly_chart(fig_pathway, use_container_width=True)

with tab4:
    st.markdown('<p class="section-header">Protein Structure Predictions</p>', unsafe_allow_html=True)
    
    # Mock protein structure data
    proteins = ['TP53', 'BRCA1', 'EGFR', 'KRAS', 'PTEN']
    confidence_scores = np.random.uniform(0.7, 0.95, len(proteins))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("AlphaFold Prediction Quality")
        protein_df = pd.DataFrame({'Protein': proteins, 'Confidence Score': confidence_scores})
        fig_protein = px.bar(protein_df, x='Protein', y='Confidence Score')
        st.plotly_chart(fig_protein, use_container_width=True)
        
        # Mock structure visualization placeholder
        st.subheader("3D Structure Visualization")
        st.info("""
        In a full implementation, this would display:
        - Interactive 3D protein structures from AlphaFold
        - Domain annotations and functional sites
        - Variant impact visualization
        """)
        
        # Placeholder for structure visualization
        st.image("https://alphafold.ebi.ac.uk/static/images/placeholder-800x600.png", 
                 caption="Predicted protein structure would appear here",
                 use_container_width=True)
    
    with col2:
        st.subheader("Domain Architecture")
        # Mock domain data
        domains = {
            'TP53': ['DNA-binding', 'Tetramerization', 'Regulatory'],
            'BRCA1': ['RING', 'BRCT'],
            'EGFR': ['Extracellular', 'Transmembrane', 'Kinase'],
            'KRAS': ['G-domain', 'Hypervariable'],
            'PTEN': ['Phosphatase', 'C2', 'C-terminal']
        }
        
        domain_list = []
        for protein, domain_set in domains.items():
            for domain in domain_set:
                domain_list.append({'Protein': protein, 'Domain': domain, 'Length': np.random.randint(50, 200)})
        
        domain_df = pd.DataFrame(domain_list)
        fig_domain = px.sunburst(domain_df, path=['Protein', 'Domain'], values='Length')
        st.plotly_chart(fig_domain, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
**OmicsAI Platform** - Prototype for multi-omics data integration and AI-powered analysis.
This demo uses synthetic data to illustrate platform capabilities.
""")