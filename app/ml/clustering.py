import pandas as pd
from sklearn.cluster import KMeans

def run_kmeans(df: pd.DataFrame, n_clusters: int = 3):
    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(df.select_dtypes(include='number'))
    return labels
