import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Elite Terminal Adaptive", layout="wide")

# FUNDAMENTALS LOADER
def load_fundamentals(path="MasterMarketData.csv"):
    import os
    import pandas as pd
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    if "Symbol" in df.columns:
        df["ticker"] = df["Symbol"].astype(str).str.upper()
    elif "ticker" in df.columns:
        df["ticker"] = df["ticker"].astype(str).str.upper()
    else:
        return None
    return df
FUNDAMENTALS_DF = load_fundamentals()
