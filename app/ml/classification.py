import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
import streamlit as st

def run_classification(df: pd.DataFrame, label_col: str, feature_cols=None):
    if feature_cols is None:
        feature_cols = df.select_dtypes(include='number').columns.drop(label_col)
    X = df[feature_cols]
    y = df[label_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    st.write(f"Accuracy: {acc:.2f}")
    st.write("Confusion Matrix:")
    st.write(cm)
    if len(set(y)) == 2:
        y_prob = clf.predict_proba(X_test)[:,1]
        auc = roc_auc_score(y_test, y_prob)
        st.write(f"ROC AUC: {auc:.2f}")
    st.write("Feature Importances:")
    st.write(pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False))
