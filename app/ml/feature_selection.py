import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
import streamlit as st

def select_top_features(df: pd.DataFrame, label_col: str, k: int = 10):
    X = df.select_dtypes(include='number')
    y = df[label_col]
    selector = SelectKBest(score_func=f_classif, k=min(k, X.shape[1]))
    selector.fit(X, y)
    top_features = X.columns[selector.get_support()]
    st.write(f"Top {len(top_features)} features:")
    st.write(top_features.tolist())
    st.write("Scores:")
    st.write(pd.Series(selector.scores_, index=X.columns).sort_values(ascending=False).head(k))
