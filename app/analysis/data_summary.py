import pandas as pd

def summarize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return summary statistics for the uploaded dataframe."""
    return df.describe(include='all')
